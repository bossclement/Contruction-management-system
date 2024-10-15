from sqlalchemy import Table, ForeignKey, Date, Column, String, Integer
from blueprints.backend.database.database import Base
from datetime import date

user_jobs_association = Table(
    'user_jobs', Base.metadata,
    Column('user_id', String(60), ForeignKey('users.username'), primary_key=True),
    Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    Column('status', String(20), nullable=False, default='pending'),
    Column('start_date', Date, nullable=False, default=date.today)
)