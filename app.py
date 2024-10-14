from flask import Flask, request, redirect, render_template, session, url_for, flash
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'JUIjdepoIOIjdfpowesopIHJpJdpjdoiHJdio#dk123'

@app.route('/')
@app.route('/home')
def home():
    return render_template('pages/index.html')

if __name__ == '__main__':
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
    app.config['SESSION_COOKIE_DOMAIN'] = 'build.com'
    app.config['SERVER_NAME'] = 'build.com:5000'
    app.run(host='build.com', port=5000, debug=True)