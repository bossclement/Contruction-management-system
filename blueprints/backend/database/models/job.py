from sqlalchemy import ForeignKey, Column, Date, String, Integer
from sqlalchemy.orm import relationship
from blueprints.backend.database.database import Base
from datetime import date
from blueprints.backend.database.models.tables import user_jobs_association

class Job(Base):
    __tablename__ = "jobs"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(1024))
    description = Column('description', String(1024))
    duration_days = Column('duration_days', Integer)
    pay_per_hour = Column('pay_per_hour', Integer)
    hours_per_day = Column('hours_per_day', Integer)
    post_date = Column(Date, default=date.today, name='post_date')
    users = relationship("User", secondary=user_jobs_association, cascade="all, delete", back_populates="jobs")

    def __init__(self, title, description, duration_days, pay_per_hour, hours_per_day, post_date=None):
        self.title = title
        self.description = description
        self.duration_days = duration_days
        self.pay_per_hour = pay_per_hour
        self.hours_per_day = hours_per_day
        self.post_date = post_date if post_date else date.today()

    def __repr__(self):
        return f"{self.id} | {self.title}"
