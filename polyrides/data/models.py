from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create a local directory to store our sqlLite database
# this URL can be swapped to any other db URL such as:
# mySQL, POSTgresql, etc.
DB_URI = 'sqlite:///./main.db'
Base = declarative_base()

# Create a model User, for our DB using 
# SQL Alchemy's declarative base.
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    last_name = Column(String(64),unique=True)
    first_name = Column(String(64),unique=True)

    def __init__(self, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name

# create all models for the current app's context
if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)