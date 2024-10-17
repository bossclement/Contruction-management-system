from sqlalchemy import Column, String, Integer, Date
from blueprints.backend.database.database import Base
from datetime import date

class Message(Base):
    __tablename__ = "messages"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    email = Column('email', String(60))
    name = Column('name', String(200))
    subject = Column('subject', String(1040))
    message = Column('message', String(1040))
    date = Column(Date, default=date.today, name='date')
    status = Column('status', String(20), default='unread')

    def __init__(self, email, name, subject, message, post_date=None, status=None):
        self.email = email
        self.name = name
        self.subject = subject
        self.message = message
        self.date = post_date if post_date else date.today()
        self.status = status if status else 'unread'

    def __repr__(self):
        return f"{self.email} | {self.subject}"