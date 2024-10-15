from flask import Flask, Blueprint, render_template, redirect, request, url_for, flash, get_flashed_messages, session
from blueprints.backend.database.dao.userDao import UserDao
from blueprints.backend.database.models.user import User
from functools import wraps
import bcrypt

app = Blueprint('backend', __name__, template_folder='templates',
                static_folder='static', static_url_path='/backend/static')

@app.route('/', subdomain='auth')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth.html')

@app.route('/login', subdomain='auth', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    user = User(username, '', password)
    response = UserDao.check_credentials(user)
    if response['status']:
        # save session
        session['user'] = username
        if remember:
            session.permanent = True
        else:
            session.permanent = False
        return redirect(url_for('backend.dashboard'))
    flash(response['msg'], 'failed')
    return redirect(url_for('backend.home'))

@app.route('/register', subdomain='auth', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    email = request.form.get('email')
    user = User(username, email, hashed_password)
    response = UserDao.create(user)
    flash(response['msg'], 'failed' if not response['status'] else 'success')
    return redirect(url_for('backend.home'))

@app.route('/dashboard')
def dashboard():
    user =  UserDao.get(session.get('user'))['user']
    if not user:
        return redirect(url_for('backend.home'))
    elif user.admin:
        return redirect(url_for('admin.home'))
    return redirect(url_for('client.home'))