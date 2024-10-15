from flask import Flask, Blueprint, render_template, redirect, request, url_for, flash, get_flashed_messages, session
from blueprints.backend.database.dao.userDao import UserDao
from blueprints.backend.database.models.user import User
from blueprints.utils.backend import login_required, subdomain_check_point
from datetime import date, timedelta

client = Blueprint('client', __name__, template_folder='templates',
                static_folder='static', static_url_path='/client/static')

@client.route('/', subdomain='dashboard')
@login_required
@subdomain_check_point
def home():
    username = session.get('user')
    res = UserDao.dashboard_info(username=username)
    if not res['status']:
        flash(res['msg'], 'failed' if not res['status'] else 'success')
    return render_template('client/base.html', username=username, category='dashboard', info=res['info'])


@client.route('/logout', subdomain='dashboard')
def logout():
    session.clear()
    return redirect(url_for('backend.home'))