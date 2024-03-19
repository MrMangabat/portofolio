## ----------------- Imports root path ----------------- ##
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Adjust the path to include the root directory


from sqlalchemy.orm import Session

from backend.databases.postgres_database import models, postgres_schemas

def get_working_experiences(db: Session):
    return db.query(models.WorkingExperiences).all()

def get_education(db: Session):
    return db.query(models.Education).all()

