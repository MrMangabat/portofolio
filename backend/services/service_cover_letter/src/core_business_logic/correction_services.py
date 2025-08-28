# backend/services/service_cover_letter/src/service_layer/correction_services.py

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from src.repositories.postgresql.CRUD_postgres import CorrectionRepository 
from src.models.database.postgresql.postgres_models import CorrectionItem, CorrectionType

"""middle layers for interacting with the database and the routes, can serve as a place to put business logic if nedded"""

## data transformations, cleaning 
class CorrectionService:
    """Provides business logic for corrections."""
    def __init__(self, db_session: Session):
        self.repository = CorrectionRepository(db_session)

    def get_corrections(self, correction_type: CorrectionType = None) -> List[CorrectionItem]:
        if correction_type:
            corrections = self.repository.get_by_type(correction_type)
        else:
            corrections = self.repository.get_all()
        return [CorrectionItem.model_validate(c) for c in corrections]

    def create_correction(self, correction: CorrectionItem) -> CorrectionItem:
        new_correction = self.repository.create(correction.text, correction.type)
        return CorrectionItem.model_validate(new_correction)

    def remove_correction(self, correction_id: UUID) -> CorrectionItem:
        # Get the correction first before deleting
        correction_to_delete = self.repository.get_by_id(correction_id)
        if not correction_to_delete:
            return None
            
        # Delete the correction
        delete_success = self.repository.delete(correction_id)
        if delete_success:
            return CorrectionItem.model_validate(correction_to_delete)
        else:
            return None
