# https://fastapi.tiangolo.com/tutorial/sql-databases/

## ----------------- Imports root path ----------------- ##
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Adjust the path to include the root directory

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from databases.postgres_database.create_database import Base

class WorkingExperiences(Base):
    # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    __tablename__ = 'working_experiences'

    we_id = Column(Integer, primary_key=True)
    job_title = Column(String(50), nullable=False)
    company_name = Column(String(50), nullable=False)
    job_description = Column(String(1000), nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)  
    image_path = Column(String(1000), nullable=False)

class Education(Base):
    # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    __tablename__ = 'education'

    edu_id = Column(Integer, primary_key=True)
    school_name = Column(String(500), nullable=False)
    degree = Column(String(500), nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    image_path = Column(String(1000), nullable=False)

class User(Base):
    # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)
    job_title = Column(String(100), nullable=False)
