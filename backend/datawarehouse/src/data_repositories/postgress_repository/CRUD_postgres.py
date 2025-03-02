# backend/jobapplication_feature/crud/job_crud.py
"""Postgres CRUD functionality"""

from sqlalchemy.orm import Session
from src.data_models.postgres_models import CorrectionORM, CorrectionType, JobListingORM, JobListingItem

class CorrectionRepository:
    """Handles database operations for corrections."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self):
        return self.db_session.query(CorrectionORM).all()

    def get_by_type(self, correction_type: CorrectionType):
        return self.db_session.query(CorrectionORM).filter(CorrectionORM.type == correction_type).all()

    def add(self, text: str, correction_type: CorrectionType):
        correction = CorrectionORM(text=text, type=correction_type)
        self.db_session.add(correction)
        self.db_session.commit()
        self.db_session.refresh(correction)
        return correction

    def delete(self, correction_id: int):
        correction = self.db_session.query(CorrectionORM).filter(CorrectionORM.id == correction_id).first()
        if correction:
            self.db_session.delete(correction)
            self.db_session.commit()
        return correction


class JoblistingsRepository:
    """Handles database operations for job listings."""
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self):
        return self.db_session.query(JobListingORM).all()

    def add(self, job_listing: JobListingItem):
        job_listing = JobListingORM(**job_listing.model_dump())
        self.db_session.add(job_listing)
        self.db_session.commit()
        self.db_session.refresh(job_listing)
        return job_listing

    def delete(self, job_listing_id: int):
        job_listing = self.db_session.query(JobListingORM).filter(JobListingORM.id == job_listing_id).first()
        if job_listing:
            self.db_session.delete(job_listing)
            self.db_session.commit()
        return job_listing
