# backend/services/service_cover_letter/src/service_layer/correction_services.py

from typing import List
from sqlalchemy.orm import Session
from src.data_repositories.postgress_repository.CRUD_postgres import CorrectionRepository 
from src.data_models.postgres_models import CorrectionItem, CorrectionType

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
        new_correction = self.repository.add(correction.text, correction.type)
        return CorrectionItem.model_validate(new_correction)

    def remove_correction(self, correction_id: int) -> CorrectionItem:
        deleted_correction = self.repository.delete(correction_id)
        if deleted_correction:
            return CorrectionItem.model_validate(deleted_correction)
        else:
            return None
