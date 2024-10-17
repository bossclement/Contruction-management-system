from flask import Flask, Blueprint, render_template, redirect, request, url_for, flash, get_flashed_messages, session
from blueprints.backend.database.dao.userDao import UserDao
from blueprints.backend.database.dao.jobDao import JobDao
from blueprints.backend.database.dao.newsletterDao import NewsLetterDao
from blueprints.backend.database.dao.messageDao import MessageDao
from blueprints.backend.database.models.job import Job
from functools import wraps
from blueprints.utils.backend import login_required, subdomain_check_point

admin = Blueprint('admin', __name__, template_folder='templates',
                static_folder='static', static_url_path='/admin/static')


def admin_dashboard_info() -> dict:
    info = {
        'total_workers': 0,
        'total_jobs': 0,
        'job_applications': 0,
        'payment_requests': 0,
        'new_messages': 0,
        'newsletters': 0,
    }
    user_res = UserDao.workers()
    if user_res['status']:
        info['total_workers'] = len(user_res['workers'])
    
    job_res = JobDao.all()
    if job_res['status']:
        info['total_jobs'] = len(job_res['jobs'])

    job_request_res = JobDao.all_requests()
    if job_res['status']:
        info['job_applications'] = len(job_request_res['requests'])
    
    payment_requests_res = JobDao.all_payments()
    if job_res['status']:
        info['payment_requests'] = len(payment_requests_res['payments'])

    new_messages_res = MessageDao.new_messages()
    if job_res['status']:
        info['new_messages'] = len(new_messages_res['messages'])

    newsletters_res = NewsLetterDao.all()
    if job_res['status']:
        info['newsletters'] = len(newsletters_res['newsletters'])
    
    return info

@admin.route('/', subdomain='admin')
@login_required
@subdomain_check_point
def home():
    username = session.get('user')
    return render_template('admin/base.html', username=username, category='dashboard', info=admin_dashboard_info())

@admin.route('/jobs', subdomain='admin')
@login_required
@subdomain_check_point
def jobs():
    username = session.get('user')
    res = JobDao.all()
    if not res['status']:
        flash(res['msg'], 'failed')
        return render_template(
            'admin/base.html',
            category='jobs'
        )
    jobs = res['jobs']
    return render_template(
        'admin/base.html',
        category='jobs',
        jobs=jobs
    )

@admin.route('/new', subdomain='admin', methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        return render_template(
            'admin/base.html',
            category='post'
        )
    title = request.form['title']
    description = request.form['description']
    duration = request.form['duration']
    pay = request.form['pay']
    hours = request.form['hours']
    job = Job(
        description=description,
        duration_days=duration,
        hours_per_day=hours,
        pay_per_hour=pay,
        title=title
    )
    res = JobDao.create(job=job)
    flash(res['msg'], 'failed' if not res['status'] else 'success')
    return redirect(url_for('admin.jobs'))

@admin.route('/edit/<int:job_id>', subdomain='admin', methods=["GET", "POST"])
@login_required
def edit(job_id):
    if request.method == "GET":
        res = JobDao.get(job_id=job_id)
        if not res['status']:
            flash(res['msg'], 'failed')
            return redirect(url_for('admin.jobs'))
        return render_template(
            'admin/base.html',
            category='post',
            job=res['job']
        )
    else:
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        pay = request.form['pay']
        hours = request.form['hours']
        res = JobDao.update(
            title=title,
            description=description,
            duration_days=duration,
            hours_per_day=hours,
            job_id=job_id,
            pay_per_hour=pay,
        )
        flash(res['msg'], 'failed' if not res['status'] else 'success')
        return redirect(url_for('admin.jobs'))
    
@admin.route('/delete/<int:job_id>', subdomain='admin')
@login_required
def delete(job_id):
    res = JobDao.delete(job_id=job_id)
    flash(res['msg'], 'failed' if not res['status'] else 'success')
    return redirect(url_for('admin.jobs'))

@admin.route('/requests', subdomain='admin')
@login_required
def requests():
    res = JobDao.all_requests()
    return render_template(
        'admin/base.html',
        category='requests',
        requests=res['requests']
    )
    
@admin.route('/logout', subdomain='admin')
def logout():
    session.clear()
    return redirect(url_for('backend.home'))