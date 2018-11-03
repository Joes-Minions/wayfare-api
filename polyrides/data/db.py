from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from polyrides.data.models import DB_URI

#  A Session establishes all 
#  conversations with the database and represents a “holding zone” 
#  for all the objects which you’ve loaded or associated with it
#  during its lifespan.
#  It provides the entrypoint to acquire a Query 
#  object, which sends queries to the database using the Session object’s 
#  current database connection, populating result rows into objects 
#  that are then stored in the Session

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
