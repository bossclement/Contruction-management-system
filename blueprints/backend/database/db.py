from sqlalchemy.orm import sessionmaker
from blueprints.backend.database.models.user import User
from blueprints.backend.database.database import Base
from blueprints.backend.database.database import engine

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
