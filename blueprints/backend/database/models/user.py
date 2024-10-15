from sqlalchemy import Column, String, Integer, Date
from blueprints.backend.database.database import Base
from datetime import date
from blueprints.backend.database.models.tables import user_jobs_association
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    username = Column('username', String(60), primary_key=True)
    email = Column('email', String(60))
    password = Column('password', String(60))
    date = Column(Date, default=date.today, name='date')
    admin = Column('admin', Integer)
    jobs = relationship("Job", secondary=user_jobs_association, cascade="all, delete", back_populates="users")

    def __init__(self, username, email, password, admin=0, creation_date=None):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        self.date = creation_date if creation_date else date.today()

    def __repr__(self):
        return "username: {0}\nemail: {1}".format(self.username, self.email)