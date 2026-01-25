# File: src/models/database/postgresql/file_metadata_models.py
"""
SQLAlchemy ORM models for enhanced file metadata management.

WHY: Extends existing PostgreSQL ORM pattern to support structured file metadata with business logic constraints
CONTRIBUTION: Provides type-safe database operations for file categorization and semantic search enhancement within service domain
HOW: Uses declarative mapping with relationships that integrate with existing MinIO storage and Qdrant vector operations
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

# Import existing connection pattern from service structure (using existing pattern)
from src.config.config_db_connections import PostgressConnection

class FileMetadataORM(PostgressConnection.Base):
    """
    ORM model for core file metadata following service architecture patterns.
    
    WHY: Provides unified interface for file attributes that integrates with existing MinIO and Qdrant workflows
    CONTRIBUTION: Serves as single source of truth for file data while maintaining compatibility with current FileUploads.vue flow
    HOW: Uses table structure that links MinIO storage with metadata for enhanced semantic search capabilities
    """
    __tablename__ = 'file_metadata'
    
    # Primary identification following existing UUID pattern
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String(255), nullable=False, index=True)  # Original filename from user upload
    file_type = Column(String(20), nullable=False, index=True)
    language = Column(String(10), nullable=False, index=True)
    schema_version = Column(String(10), default='1.0', nullable=False)
    
    # Audit fields following existing pattern
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # MinIO integration fields linking to existing storage
    minio_bucket = Column(String(50), nullable=False)  # cover-letters, cv, images
    minio_filename = Column(String(255), nullable=False)  # UUID.extension format
    original_content_type = Column(String(100))  # From FastAPI UploadFile
    file_size = Column(Integer)  # Bytes, for UI display
    
    # Qdrant integration
    qdrant_point_id = Column(UUID(as_uuid=True))  # Links to vector database point
    
    # Relationships to type-specific metadata
    template_metadata = relationship("TemplateMetadataORM", back_populates="file_metadata", cascade="all, delete-orphan", uselist=False)
    cv_metadata = relationship("CVMetadataORM", back_populates="file_metadata", cascade="all, delete-orphan", uselist=False)
    
    # Constraints matching business rules
    __table_args__ = (
        CheckConstraint("file_type IN ('template', 'cv', 'application')", name='ck_file_metadata_type'),
        CheckConstraint("language IN ('english', 'danish')", name='ck_file_metadata_language'),
    )
    
    def __repr__(self):
        """
        WHY: Provides readable representation for debugging file operations and logging
        CONTRIBUTION: Aids development and troubleshooting of enhanced file management workflow
        HOW: Returns formatted string with key identifying attributes for system monitoring
        """
        return f"<FileMetadata(id={self.id}, filename='{self.filename}', type='{self.file_type}')>"

class TemplateMetadataORM(PostgressConnection.Base):
    """
    ORM model for cover letter template business logic and categorization.
    
    WHY: Stores template-specific attributes needed for jobtype filtering and LLM context generation
    CONTRIBUTION: Enables enhanced semantic search with metadata filtering for improved template recommendations
    HOW: Uses foreign key relationship with JSON arrays for flexible categorization while maintaining referential integrity
    """
    __tablename__ = 'template_metadata'
    
    file_id = Column(UUID(as_uuid=True), ForeignKey('file_metadata.id', ondelete='CASCADE'), primary_key=True)
    jobtype = Column(String(100), nullable=False, index=True)  # Links to jobtypes table
    industry_sectors = Column(JSONB, default=list, nullable=False)  # Multi-select industry array
    template_subtype = Column(String(50), default='cover_letter', nullable=False)
    company_size_target = Column(String(20), default='any', nullable=False)
    
    # Usage tracking for recommendation engine
    last_used_at = Column(DateTime)  # Updated when template used in generation
    effectiveness_score = Column(Float, default=0.0)  # Future ML ranking feature
    
    # Relationship back to core file data
    file_metadata = relationship("FileMetadataORM", back_populates="template_metadata")
    
    # Business logic constraints
    __table_args__ = (
        CheckConstraint("template_subtype IN ('cover_letter', 'application')", name='ck_template_subtype'),
        CheckConstraint("company_size_target IN ('startup', 'mid', 'enterprise', 'any')", name='ck_company_size'),
        CheckConstraint("effectiveness_score >= 0.0 AND effectiveness_score <= 1.0", name='ck_effectiveness_range'),
    )
    
    def __repr__(self):
        return f"<TemplateMetadata(file_id={self.file_id}, jobtype='{self.jobtype}')>"

class CVMetadataORM(PostgressConnection.Base):
    """
    ORM model for curriculum vitae metadata and content extraction results.
    
    WHY: Captures CV-specific data for role matching and experience-based template selection
    CONTRIBUTION: Supports future CV section extraction and provides context for LLM-generated cover letters
    HOW: Uses JSON columns for flexible skill arrays while maintaining structured experience data for business logic
    """
    __tablename__ = 'cv_metadata'
    
    file_id = Column(UUID(as_uuid=True), ForeignKey('file_metadata.id', ondelete='CASCADE'), primary_key=True)
    primary_roles = Column(JSONB, default=list, nullable=False)  # User-defined or extracted roles
    experience_years = Column(Integer)  # Total professional experience
    industries_mentioned = Column(JSONB, default=list, nullable=False)  # Auto-extracted from CV text
    skills_extracted = Column(JSONB, default=list, nullable=False)  # Text processing results
    is_current_cv = Column(Boolean, default=False, index=True)  # Primary CV flag for user
    sections_extracted = Column(JSONB, default=dict, nullable=False)  # Future drag-drop builder data
    
    # Processing status for async operations
    extraction_completed = Column(Boolean, default=False, nullable=False)
    extraction_error = Column(Text)  # Error logging for failed processing
    
    # Relationship back to core file data
    file_metadata = relationship("FileMetadataORM", back_populates="cv_metadata")
    
    # Data validation constraints
    __table_args__ = (
        CheckConstraint("experience_years >= 0 AND experience_years <= 50", name='ck_experience_years'),
    )
    
    def __repr__(self):
        return f"<CVMetadata(file_id={self.file_id}, experience={self.experience_years}y, current={self.is_current_cv})>"

class JobtypeORM(PostgressConnection.Base):
    """
    ORM model for job type lookup data following existing corrections pattern.
    
    WHY: Maintains standardized job type vocabulary for dropdown population in FileUploads.vue interface
    CONTRIBUTION: Ensures data consistency for template categorization and provides foundation for jobtype analytics
    HOW: Uses unique constraint and lifecycle management similar to existing corrections pattern
    """
    __tablename__ = 'jobtypes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))  # Grouping for UI organization
    is_active = Column(Boolean, default=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    description = Column(Text)  # Human-readable description for UI tooltips
    
    def __repr__(self):
        return f"<Jobtype(id={self.id}, name='{self.name}', active={self.is_active})>"

class IndustryORM(PostgressConnection.Base):
    """
    ORM model for industry categorization lookup data.
    
    WHY: Provides controlled vocabulary for industry tagging across template and CV categorization
    CONTRIBUTION: Enables industry-based filtering in semantic search and supports future market analysis
    HOW: Mirrors jobtype pattern for consistency in lookup table management and API responses
    """
    __tablename__ = 'industries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    sector = Column(String(50))  # Higher-level industry grouping
    is_active = Column(Boolean, default=True, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    description = Column(Text)  # Description for UI and categorization
    
    def __repr__(self):
        return f"<Industry(id={self.id}, name='{self.name}', sector='{self.sector}')>"