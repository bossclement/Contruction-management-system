from blueprints.backend.database.db import session
from blueprints.backend.database.models.user import User
from blueprints.backend.database.models.job import Job
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, select
from blueprints.backend.database.models.tables import user_jobs_association
from datetime import timedelta

class JobDao:

    @staticmethod
    def create(job:Job):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            session.add(job)
            session.commit()
            msg = "Job created Successfully"
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def get(job_id):
        status = False
        found = None
        msg = "Something went wrong"
        try:
            result = session.query(Job).filter_by(id=job_id)
            found = result.first()
            status = isinstance(found, Job)
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'job': found}
    
    @staticmethod
    def all():
        status = False
        jobs = []
        msg = "No jobs found"
        try:
            result = session.query(Job).all()
            status = isinstance(result, list)
            jobs = result
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'jobs': jobs}
    
    @staticmethod
    def update(job_id, title=None, description=None, duration_days=None, pay_per_hour=None, hours_per_day=None):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            job = session.query(Job).filter_by(id=job_id).first()
            if job:
                if title is not None:
                    job.title = title
                if description is not None:
                    job.description = description
                if duration_days is not None:
                    job.duration_days = duration_days
                if pay_per_hour is not None:
                    job.pay_per_hour = pay_per_hour
                if hours_per_day is not None:
                    job.hours_per_day = hours_per_day

                session.commit()
                status = True
                msg = "Job updated successfully"
            else:
                msg = "Job not found"
        except IntegrityError as e:
            session.rollback()
            msg = "Integrity error occurred"
        except Exception as e:
            session.rollback()
            msg = e.args[0]

        return {'status': status, 'msg': msg}
    
    @staticmethod
    def delete(job_id):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            job = session.query(Job).filter_by(id=job_id).first()
            if job:
                # Delete all associated relationships in user_jobs_association
                session.execute(
                    user_jobs_association.delete().where(user_jobs_association.c.job_id == job_id)
                )
                
                # Delete the job itself
                session.delete(job)
                
                # Commit the changes to the database
                session.commit()
                status = True
                msg = "Job deleted successfully"
            else:
                msg = "Job not found"
        except IntegrityError as e:
            session.rollback()
            msg = "Integrity error occurred"
        except Exception as e:
            session.rollback()
            msg = e.args[0]

        return {'status': status, 'msg': msg}
    
    @staticmethod
    def all_requests():
        status = False
        msg = "Something went wrong, Please try again"
        requests = []
        try:
            query = select(user_jobs_association).where(user_jobs_association.c.status == 'pending')
            # Execute the query
            result = session.execute(query).fetchall()

            # format results
            for row in result:
                # get user
                user = session.query(User).filter_by(username=row[0]).first()
                if not user:
                    return {'status': False, 'msg': 'failed to get user'}
                
                # get job
                job_res = JobDao.get(row[1])
                if not job_res['status']:
                    return job_res
                
                # add data to request
                requests.append({
                    'user': user,
                    'job': job_res['job'],
                    'date': row[3].strftime("%Y - %m - %d").replace(' 0', ' ')
                })
            status = True
            msg = "Success"
        except Exception as e:
            session.rollback()
            msg = e.args[0]

        return {'status': status, 'msg': msg, 'requests': requests}
    
    @staticmethod
    def all_payments():
        status = False
        msg = "Something went wrong, Please try again"
        payments = []
        try:
            query = select(user_jobs_association).where(user_jobs_association.c.status == 'requested')
            # Execute the query
            result = session.execute(query).fetchall()

            # format results
            for row in result:
                # get user
                user = session.query(User).filter_by(username=row[0]).first()
                if not user:
                    return {'status': False, 'msg': 'failed to get user'}
                
                # get job
                job_res = JobDao.get(row[1])
                if not job_res['status']:
                    return job_res
                
                # add data to request
                job = job_res['job']
                payments.append({
                    'user': user,
                    'job': job,
                    'application_date': row[3].strftime("%Y - %m - %d").replace(' 0', ' '),
                    'completion_date': (row[3] + timedelta(days=job.duration_days)).strftime("%Y - %m - %d").replace(' 0', ' '),
                    'amount': job.duration_days * (job.hours_per_day * job.pay_per_hour)
                })
            status = True
            msg = "Success"
        except Exception as e:
            session.rollback()
            msg = e.args[0]

        return {'status': status, 'msg': msg, 'payments': payments}