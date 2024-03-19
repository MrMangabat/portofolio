## ----------------- Imports root path ----------------- ##
import sys
import os
from pathlib import Path
ROOT = sys.path.append(str(Path(__file__).parent.parent.parent))  # Adjust the path to include the root directory


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_POSTGRES_URL = 'postgresql+psycopg2://mangabat:3810@localhost:5432/bumstuff_database'

# create SQLAlchemy engine and session
postgres_engine = create_engine(SQLALCHEMY_POSTGRES_URL)

#the actual database session once instansiated
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = postgres_engine)

#used to create base class for models
Base = declarative_base()