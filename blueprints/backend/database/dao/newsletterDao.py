from blueprints.backend.database.db import session
from blueprints.backend.database.models.newsletter import NewsLetter
from sqlalchemy.exc import IntegrityError

class NewsLetterDao:

    @staticmethod
    def create(newsletter:NewsLetter):
        status = False
        msg = "Something went wrong, Please try again"
        try:
            session.add(newsletter)
            session.commit()
            msg = "Subscribed to news letter successful"
            status = True
        except IntegrityError as e:
            session.rollback()
            msg = "Email already used"
        except Exception as e:
            session.rollback()
            msg = e.args[0]
        return {'status': status, 'msg': msg}
    
    @staticmethod
    def all():
        status = False
        newsletters = []
        msg = "No entries found"
        try:
            result = session.query(NewsLetter).all()
            status = isinstance(result, list)
            newsletters = result
            status = True
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg, 'newsletters': newsletters}
    
    @staticmethod
    def delete(email):
        status = False
        msg = "Email not found"
        try:
            newsletter = session.query(NewsLetter).filter_by(email=email).first()
            if newsletter is not None:
                session.delete(newsletter)
                session.commit()
                msg = "Entry removed successfully"
                status = True
        except Exception as e:
            msg = e.args[0]
            session.rollback()
        return {'status': status, 'msg': msg}