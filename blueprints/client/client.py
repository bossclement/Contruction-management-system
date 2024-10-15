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

@client.route('/apply', subdomain='dashboard')
@login_required
def apply():
    username = session.get('user')
    return render_template('client/base.html', category='apply', jobs=UserDao.available_jobs(username)['jobs'])

@client.route('/apply/<int:job_id>', subdomain='dashboard')
@login_required
def apply_job(job_id):
    username = session.get('user')
    res = UserDao.add_job(username=username, job_id=job_id)
    flash(res['msg'], 'failed' if not res['status'] else 'success')
    return redirect(url_for('client.apply'))

@client.route('/jobs', subdomain='dashboard')
@login_required
@subdomain_check_point
def jobs():
    username = session.get('user')
    res = UserDao.get_user_jobs(username=username)
    if not res['status']:
        flash(res['msg'], 'failed' if not res['status'] else 'success')
        return render_template(
            'client/base.html',
            category='jobs'
        )
    jobs = res['user_jobs']
    return render_template(
        'client/base.html',
        category='jobs',
        jobs=jobs
    )

@client.route('/payment/<int:job_id>', subdomain='dashboard')
@login_required
def payment_request(job_id):
    username = session.get('user')
    res = UserDao.get_user_jobs(username=username)
    if not res['status']:
        flash(res['msg'], 'failed' if not res['status'] else 'success')
        return render_template(
            'client/base.html',
            category='jobs'
        )

    # find the job requested for payment
    jobs = res['user_jobs']
    job = None
    for x in jobs:
        if x['job'].id == job_id:
            job = x
            break
    
    # check if job is in approved status
    if job and job['status'] == 'approved':
        res = UserDao.update_job_status(
            job_id=job['job'].id,
            username=username,
            status_value='requested'
        )
        if not res['status']:
            flash(res['msg'], 'failed' if not res['status'] else 'success')
            return render_template(
                'client/base.html',
                category='jobs',
                jobs=jobs
            )
        else:
            flash('Payment request successful', 'success')
    else:
        flash('Failed to update job status', 'failed')

    return redirect(url_for('client.jobs'))


@client.route('/logout', subdomain='dashboard')
def logout():
    session.clear()
    return redirect(url_for('backend.home'))