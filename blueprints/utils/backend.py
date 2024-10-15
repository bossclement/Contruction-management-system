from flask import redirect, url_for, flash, session, request
from blueprints.backend.database.dao.userDao import UserDao
from blueprints.backend.database.models.user import User
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if session is alive
        if 'user' not in session:
            flash('Login is required to access this page', 'failed')
            return redirect(url_for('backend.home'))
        
        # check if exists
        response = UserDao.get(session.get('user'))
        if not response['status']:
            session.clear()
            flash(response['msg'], 'failed')
            return redirect(url_for('backend.home'))
        
        return f(*args, **kwargs)
    return decorated_function

def subdomain_check_point(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get user
        response = UserDao.get(session.get('user'))
        user = response['user']
        if not response['status']:
            session.clear()
            flash(response['message'], 'failed')
            return redirect(url_for('backend.home'))
        
        # check subdomain
        subdomain = request.host.split('.')[0]
        if subdomain == 'dashboard':
            if user.admin:
                return redirect(url_for('admin.home'))
        elif subdomain == 'admin':
            if not user.admin:
                return redirect(url_for('client.home'))
        else:
            return redirect(url_for('backend.home'))
        
        return f(*args, **kwargs)
    return decorated_function