from flask import Flask, request, render_template

app = Flask(__name__)

class ConfigClass(object):
    SECRET_KEY = b'p\xe3\\l\xd5\xee\\6\xaa\xc4\xbc\xd0n\x95\xea\xfe\x00z\x82[t\x1bs\x85? \xe11\x98\xf9\xda@\x83\x1f\xa0"\xa3\xdf\xe1z\xe6R\xcc/\xafM5z\xdcY\xbe\xa9tqvj\x85\xe4\xe1\xaf\x9b\x07\x88.'

app.config.from_object(__name__+'.ConfigClass')

# * Test route
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/discover', methods=['GET'])
def discover():
    return render_template('discover.html')

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html')