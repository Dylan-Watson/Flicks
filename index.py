from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_user.signals import user_registered
from json import dumps, loads
import sqlite3
import string 
import random

app = Flask(__name__)

class ConfigClass(object):
    SECRET_KEY = 'p\xe3\\l\xd5\xee\\6\xaa\xc4\xbc\xd0n\x95\xea\xfe\x00z\x82[t\x1bs\x85? \xe11\x98\xf9\xda@\x83\x1f\xa0"\xa3\xdf\xe1z\xe6R\xcc/\xafM5z\xdcY\xbe\xa9tqvj\x85\xe4\xe1\xaf\x9b\x07\x88.'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/db/flicks.db'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Flicks"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False        # Enable email authentication
    USER_ENABLE_USERNAME = True    # Disable username authentication

app.config.from_object(__name__+'.ConfigClass')
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

user_manager = UserManager(app, db, User)
db.create_all()


# * Test route
@app.route('/',methods=['GET'])
@login_required
def home():
    return redirect(url_for('discover'))
    # return render_template('index.html')

@app.route('/discover', methods=['GET'])
@login_required
def discover():
    return render_template('discover.html')

@app.route('/results', methods=['GET'])
@login_required
def results():
    code = request.args.get('code',None)
    if(code is None):
        return 'error'
    c = connect()

    
    disconnect(c)
    return render_template('results.html')

@app.route('/gcreate', methods=['GET'])
@login_required
def gcreate():
    c = connect()
    found = True
    while(found == True):
        code = generateString()
        c.execute('select * from groups where code = ?', (code,))
        res = c.fetchone()
        if(res is None):
            found = False
    users = [current_user.id]
    c.execute('insert into groups (code, users) values (?, ?)', (code,dumps(users)))
    c.execute('select groups from attributes where user_id =(?)', (current_user.id,))
    groups = loads(c.fetchone()[0])
    if(len(groups) != 0):
        for v in groups:
            c.execute('delete from groups where code=(?)', (v,))
    groups = [code]
    print(dumps(groups))
    c.execute('update attributes set groups=(?) where user_id=(?)', (dumps(groups), current_user.id))
    disconnect(c)
    return render_template('gcreate.html',code=code, person=current_user.username)

@app.route('/gjoin', methods=['GET'])
@login_required
def gjoin():
    return render_template('gjoin.html')

@app.route('/joinsuccess', methods=['GET'])
@login_required
def joinsuccess():
    return render_template('joinsuccess.html')

@app.route('/search', methods=['GET'])
@login_required
def search():
    return render_template('search.html')

@app.route('/searchresults', methods=['GET'])
@login_required
def searchresults():
    return render_template('searchresults.html')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    c = connect()
    user_id = (current_user.id,)
    c.execute('SELECT * FROM attributes WHERE user_id=?',user_id)
    print(c.fetchone())
    return render_template('profile.html', username=current_user.username)
    disconnect()

# region AJAX

@app.route('/join-group', methods=['POST'])
@login_required
def join_group():
    code = request.args.get('code',None)
    if(code is None):
        return 'error code 1'
    c = connect()
    c.execute('select users from groups where code=(?)',(code,))
    res = c.fetchone()
    if(res is None):
        disconnect(c)
        return 'error code 2'
    users = loads(res[0])
    users.append(current_user.id)
    c.execute('update groups set users=(?) where code=(?)', (dumps(users), code))
    c.execute('select groups from attributes where user_id=(?)', (current_user.id,))
    groups = loads(c.fetchone()[0])
    if(groups is None):
        groups = [code]
    else:
        groups.append(code)
    c.execute('update attributes set groups=(?) where user_id=(?)', (dumps(groups), current_user.id))
    disconnect(c)
    return 'success' 

@app.route('/check-people', methods=['GET'])
@login_required
def check_people():
    code = request.args.get('code',None)
    if(code is None):
        return 'error code 1'
    c = connect()
    c.execute('select users from groups where code=(?)',(code,))
    res = c.fetchone()
    if(res is None):
        disconnect(c)
        return 'error code 2'
    users = loads(res[0])
    usernames = []
    for v in users:
        if(v == current_user.id):
            continue
        c.execute('select username from users where id=(?)',(v,))
        res = c.fetchone()
        if(res is None):
            return 'error code 3'
        usernames.append(res)
    disconnect(c)
    return dumps(usernames)

# endregion

# region Utility Functions

def connect():
    sql = sqlite3.connect('static/db/flicks.db', isolation_level=None)
    c = sql.cursor()
    return c

def disconnect(c):
    try:
        c.close()
    except:
        print('Oops!')

def generateString():
    # initializing size of string  
    N = 4
    
    # using random.choices() 
    # generating random strings  
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = N))
    return res

# endregion

# region Event Handlers

@user_registered.connect_via(app)
def track_registration(sender, user, **extra):
    c = connect()
    user_id = user.id
    c.execute('INSERT into attributes (user_id,groups) VALUES (?,?)',(user_id,dumps([])))
    disconnect(c)

# endregion

# region SQL Queries

# endregion