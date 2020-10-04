from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_user.signals import user_registered
import sqlite3

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
    return render_template('results.html')

@app.route('/gcreate', methods=['GET'])
@login_required
def gcreate():
    return render_template('gcreate.html')

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


@app.route('/profile', methods=['GET'])
def profile():
    c = connect()
    user_id = (current_user.id,)
    c.execute('SELECT * FROM attributes WHERE user_id=?',user_id)
    print(c.fetchone())
    return render_template('profile.html', username=current_user.username)
    disconnect()

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
# endregion

# region Event Handlers

@user_registered.connect_via(app)
def track_registration(sender, user, **extra):
    c = connect()
    user_id = (user.id,)
    c.execute('INSERT into attributes (user_id) VALUES (?)',user_id)
    disconnect(c)

# endregion

# region SQL Queries

# endregion