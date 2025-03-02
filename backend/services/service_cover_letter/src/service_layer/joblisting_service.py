# backend/jobapplication_feature/services/job_listing_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from src.data_models.postgres_models import JobListingItem
from src.data_repositories.postgress_repository.CRUD_postgres import JoblistingsRepository

class JobListingService:
    """Provides business logic for job listings."""

    def __init__(self, db_session: Session):
        self.repository = JoblistingsRepository(db_session)

    def get_all_job_listings(self) -> List[JobListingItem]:
        """Retrieve all job listings."""
        job_listings = self.repository.get_all()
        return [JobListingItem.model_validate(job) for job in job_listings]

    def create_job_listing(self, job_listing: JobListingItem) -> JobListingItem:
        """Create a new job listing."""
        new_job_listing = self.repository.add(job_listing)
        return JobListingItem.model_validate(new_job_listing)

    def delete_job_listing(self, job_listing_id: int) -> Optional[JobListingItem]:
        """Delete a job listing by ID."""
        deleted_job_listing = self.repository.delete(job_listing_id)
        if deleted_job_listing:
            return JobListingItem.model_validate(deleted_job_listing)
        else:
            return None
