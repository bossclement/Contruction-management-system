from flask import Flask, request, redirect, render_template, session, url_for, flash
from datetime import timedelta
from blueprints.backend.backend import app as backend
from blueprints.client.client import client


app = Flask(__name__)
app.secret_key = 'JUIjdepoIOIjdfpowesopIHJpJdpjdoiHJdio#dk123'
app.register_blueprint(backend)
app.register_blueprint(client)

@app.route('/')
@app.route('/home')
def home():
    return render_template('pages/index.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

if __name__ == '__main__':
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
    app.config['SESSION_COOKIE_DOMAIN'] = 'build.com'
    app.config['SERVER_NAME'] = 'build.com:5000'
    app.run(host='build.com', port=5000, debug=True)