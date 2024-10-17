from blueprints.backend.database.db import session
from blueprints.backend.database.models.message import Message

class MessageDao:

    @staticmethod
    def create(message:Message):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            session.add(message)
            session.commit()
            msg = "Sent successfully"
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def get(id):
        status = False
        msg = "Message not found"
        message = None
        try:
            message = session.query(Message).filter_by(id=id).first()
            message.status = 'read'
            session.commit()
            msg = "Successful"
            status = True
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg, 'message': message}
    
    @staticmethod
    def all():
        status = False
        messages = []
        msg = "No entries found"
        try:
            result = session.query(Message).all()
            status = isinstance(result, list)
            messages = result
            status = True
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'messages': messages}
    
    @staticmethod
    def new_messages():
        status = False
        messages = []
        msg = "No entries found"
        try:
            result = session.query(Message).filter_by(status='unread').all()
            status = isinstance(result, list)
            messages = result
            status = True
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'messages': messages}
    
    @staticmethod
    def delete(id):
        status = False
        msg = "Message not found"
        try:
            message = session.query(Message).filter_by(id=id).first()
            if message is not None:
                session.delete(message)
                session.commit()
                msg = "Entry removed successfully"
                status = True
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg}