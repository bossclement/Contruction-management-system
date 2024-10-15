from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
user = 'clement'
host = '127.0.0.1:3306'
password = 'hello world123'
database = 'construction_management_db'
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, database))
