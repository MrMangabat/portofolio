# backend/services/service_cover_letter/src/routes/routes_corrections.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.config_db_connections import PostgressConnection
from src.models.database.postgresql.postgres_models import CorrectionItem, CorrectionType
from src.core_business_logic.correction_services import CorrectionService

router = APIRouter()

def get_correction_service(db: Session = Depends(PostgressConnection.get_db)) -> CorrectionService:
    return CorrectionService(db)

@router.get("", response_model=List[CorrectionItem])
def read_corrections(
    correction_type: Optional[CorrectionType] = None,
    service: CorrectionService = Depends(get_correction_service)
) -> List[CorrectionItem]:
    return service.get_corrections(correction_type)

@router.post("", response_model=CorrectionItem)
def create_correction(
    correction: CorrectionItem,
    service: CorrectionService = Depends(get_correction_service)
) -> CorrectionItem:
    try:
        return service.create_correction(correction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{correction_id}", response_model=CorrectionItem)
def remove_correction(
    correction_id: UUID,
    service: CorrectionService = Depends(get_correction_service)
) -> CorrectionItem:
    deleted_correction = service.remove_correction(correction_id)
    if not deleted_correction:
        raise HTTPException(status_code=404, detail="Correction not found")
    return deleted_correction
