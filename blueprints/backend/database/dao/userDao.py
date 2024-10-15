from blueprints.backend.database.db import session
from blueprints.backend.database.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from blueprints.backend.database.models.tables import user_jobs_association
from datetime import timedelta
import bcrypt

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