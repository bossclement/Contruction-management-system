from blueprints.backend.database.db import session
from blueprints.backend.database.models.user import User
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
import bcrypt
from blueprints.backend.database.models.job import Job
from blueprints.backend.database.dao.jobDao import JobDao
from blueprints.backend.database.models.tables import user_jobs_association

class UserDao:

    @staticmethod
    def create(user:User):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            if len(user.password) < 10:
                return {'status': False, 'msg': 'Password must be 10 characters long.'}
            session.add(user)
            session.commit()
            msg = "Registration successful, now log in"
            status = True
        except IntegrityError as e:
            session.rollback()
            msg = "Username already used"
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def delete(username:str) -> dict:
        status = False
        msg = "Something went wrong, Please try again"
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return {'status': False, 'msg': 'User not found'}
            session.delete(user)
            session.commit()
            msg = "User deleted successfully"
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def check_credentials(user:User):
        status = False
        msg = "Invalid credentials"
        found = None
        try:
            result = session.query(User).filter_by(username=user.username)
            found = result.first()
            status = found and bcrypt.checkpw(user.password.encode('utf-8'), found.password.encode('utf-8'))
        except Exception as e:
            print(e)
            msg = e.args[0]
            session.rollback()
            pass
        return {'status': status, 'msg': msg, 'user': found}
    
    @staticmethod
    def get(username):
        status = False
        msg = "Session expired, please login"
        found = None
        try:
            result = session.query(User).filter_by(username=username)
            found = result.first()
            status = isinstance(found, User)
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'user': found}
    
    @staticmethod
    def workers():
        status = False
        msg = "Something went wrong, Please try again."
        workers = []
        try:
            workers = session.query(User).filter_by(admin=0).all()
            status = isinstance(workers, list)
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'workers': workers}
    
    @staticmethod
    def add_job(username:str, job_id:int):
        status = False
        msg = "Could not add job to user"
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return {'status': False, 'msg': "User not found"}

            res = JobDao.get(job_id=job_id)
            if not res['status']:
                return {'status': False, 'msg': res['msg']}
            
            job = res['job']
            user.jobs.append(job)
            session.commit()
            status = True
            msg = "Applied job successfully"
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def remove_job(username:str, job_id:int):
        status = False
        msg = "Could not remove job from user"
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return {'status': False, 'msg': "User not found"}

            res = JobDao.get(job_id=job_id)
            if not res['status']:
                return {'status': False, 'msg': res['msg']}
            
            job = res['job']
            user.jobs.remove(job)
            session.commit()
            status = True
            msg = "Removed job successfully"
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def get_user_jobs(username):
        status = False
        msg = "Failed to get user jobs"
        user_jobs = []
        try:
            results = session.execute(
                user_jobs_association.select().where(
                    user_jobs_association.c.user_id == username,
                )
            ).all()
            if results:
                for result in results:
                    res = JobDao.get(result[1])
                    if not res['status']:
                        return {'status': False, 'msg': res['msg']}
                    _job = res['job']
                    x = {
                        'job': _job,
                        'start_date': result[3].strftime("%Y - %m - %d").replace(' 0', ' '),
                        'end_date': (timedelta(days=_job.duration_days) + result[3]).strftime("%Y - %m - %d").replace(' 0', ' '),
                        'income': _job.duration_days * (_job.hours_per_day * _job.pay_per_hour),
                        'status': result[2]
                    }
                    user_jobs.append(x)
            msg = 'Success'
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg, 'user_jobs': user_jobs}
    
    @staticmethod
    def update_job_status(username, job_id, status_value):
        status = False
        msg = "Failed to update status"
        try:
            session.execute(
                user_jobs_association.update().where(
                    user_jobs_association.c.user_id == username,
                    user_jobs_association.c.job_id == job_id
                ).values(status=status_value)
            )
            session.commit()
            status = True
            msg = 'Successful'
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def available_jobs(username):
        status = False
        msg = "No jobs available"
        jobs = []
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return {'status': False, 'msg': "User not found"}
            
            response = JobDao.all()
            if not response['status']:
                return {'status': False, 'msg': response['msg']}
            
            list_jobs = response['jobs']
            for jb in list_jobs:
                if jb.id not in [x.id for x in user.jobs]:
                    jobs.append(jb)
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg, 'jobs': jobs}
    
    @staticmethod
    def dashboard_info(username):
        status = False
        msg = "Failed to get dashboard info"
        info = {
            'total_jobs': 0,
            'active_jobs': 0,
            'completed_jobs': 0,
            'net': 0
        }
        try:
            user_jobs_res = UserDao.get_user_jobs(username=username)
            if not user_jobs_res['status']:
                return user_jobs_res
            user_jobs = user_jobs_res['user_jobs']

            # filter jobs
            completed_jobs = []
            for x in user_jobs:
                # get active jobs
                if x['status'] != 'canceled' and x['status'] != 'completed':
                    info['active_jobs'] += 1
            
                # get completed jobs
                if x['status'] == 'completed':
                    completed_jobs.append(x)
            
            # set completed job count
            info['completed_jobs'] = len(completed_jobs)

            # calculate the net profit
            for i in completed_jobs:
                info['net'] += i['income']
            
            # get all jobs
            all_jobs_res = JobDao.all()
            if not all_jobs_res['status']:
                return all_jobs_res
            info['total_jobs'] = len(all_jobs_res['jobs'])
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg, 'info': info}