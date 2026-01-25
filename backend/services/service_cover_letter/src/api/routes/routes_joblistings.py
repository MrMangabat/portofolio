# backend/services/service_cover_letter/src/api/routes/routes_joblistings.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.connections.postgres_connection import PostgresConnection
from src.data_models.databases.postgres.postgres_models import JobListingItem
from src.service_layer.joblisting_service import JobListingService

router = APIRouter()

def get_job_listing_service(db: Session = Depends(PostgresConnection.get_db)) -> JobListingService:
    return JobListingService(db)

@router.get("", response_model=List[JobListingItem])
def read_job_listings(
    service: JobListingService = Depends(get_job_listing_service)
) -> List[JobListingItem]:
    return service.get_all_job_listings()
