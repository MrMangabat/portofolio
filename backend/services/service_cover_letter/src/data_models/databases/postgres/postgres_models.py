# backend/services/service_cover_letter/src/data_models/databases/postgres/postgres_models.py


## external modules
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import datetime
import uuid

## Internal modules
from src.config.connections.postgres_connection import PostgresConnection

# CorrectionType Enum: Defines the possible types for corrections.
class CorrectionType(PyEnum):
    word = "word"
    sentence = "sentence"
    skill = "skill"

class CorrectionORM(PostgresConnection.Base):
    __tablename__ = 'corrections'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    text = Column(String, index=True, nullable=False)
    type = Column(
        Enum(CorrectionType,
             values_callable = lambda x: [e.value for e in x],
             native_enum = False),
        index=True, nullable=False)

class CorrectionItem(BaseModel):
# Enum Matching: Ensure that the CorrectionType enum matches between SQLAlchemy and Pydantic models.
# Optional id: The id is optional for input (creation) and will be provided by the database.
    id: Optional[uuid.UUID] = None
    text: str
    type: CorrectionType

    model_config = ConfigDict(from_attributes=True)

class JobListingORM(PostgresConnection.Base):
    __tablename__ = 'joblistings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    requirements = Column(String)
    expected_experience = Column(String)
    last_chance = Column(DateTime, nullable=True)
    listing = Column(String)
    link = Column(String)
    date_posted = Column(DateTime, default=datetime.now)
    location = Column(String, index=True)
    country = Column(String)# Add other fields as necessary

class JobListingItem(BaseModel):
    id: Optional[uuid.UUID] = None
    title: str
    company: str
    requirements: str
    expected_experience: str
    last_chance: Optional[datetime] = None
    listing: str
    link: str
    date_posted: Optional[datetime] = None
    location: str
    country: str

    model_config = ConfigDict(from_attributes=True)
