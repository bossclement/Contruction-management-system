from sqlalchemy import Column, String, Integer
from blueprints.backend.database.database import Base

class NewsLetter(Base):
    __tablename__ = "news_letters"
    email = Column('email', String(60), primary_key=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"{self.email}"