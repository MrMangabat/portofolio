from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.config_db_connections import PostgressConnection
from src.data_models.postgres_models import JobListingItem
from src.service_layer.joblisting_service import JobListingService

router = APIRouter()

def get_job_listing_service(db: Session = Depends(PostgressConnection.get_db)) -> JobListingService:
    return JobListingService(db)

@router.get("", response_model=List[JobListingItem])
def read_job_listings(
    service: JobListingService = Depends(get_job_listing_service)
) -> List[JobListingItem]:
    return service.get_all_job_listings()
