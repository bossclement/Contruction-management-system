from flask import Flask, request, redirect, render_template, session, url_for, flash
from datetime import timedelta
from blueprints.backend.backend import app as backend
from blueprints.client.client import client
from blueprints.admin.admin import admin
from blueprints.backend.database.dao.newsletterDao import NewsLetterDao
from blueprints.backend.database.models.newsletter import NewsLetter


app = Flask(__name__)
app.secret_key = 'JUIjdepoIOIjdfpowesopIHJpJdpjdoiHJdio#dk123'
app.register_blueprint(backend)
app.register_blueprint(client)
app.register_blueprint(admin)

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

@app.route('/dashboard')
def dashboard():
    return redirect(url_for('backend.dashboard'))

@app.route('/newletter', methods=["POST"])
def newletter():
    email = request.form.get('email', None)
    if email:
        newsletter = NewsLetter(email=email)
        res = NewsLetterDao.create(newsletter=newsletter)
        flash(res['msg'], 'failed' if not res['status'] else 'success')
    return redirect(request.referrer or url_for('home'))

if __name__ == '__main__':
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
    app.config['SESSION_COOKIE_DOMAIN'] = 'build.com'
    app.config['SERVER_NAME'] = 'build.com:5000'
    app.run(host='build.com', port=5000, debug=True)