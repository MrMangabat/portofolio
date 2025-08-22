# File: src/repositories/postgresql/file_metadata_repository.py
"""
PostgreSQL repository for file metadata management following TDD test behaviors.

WHY: Implements the CRUD operations validated by the comprehensive test suite
CONTRIBUTION: Provides database access layer that satisfies all 5 TDD test behaviors
HOW: Uses SQLAlchemy ORM with proper transaction management and relationship handling
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.config.config_db_connections import PostgressConnection
from src.models.database.postgresql.file_metadata_models import (
    FileMetadataORM,
    TemplateMetadataORM,
    CVMetadataORM,
    JobtypeORM,
    IndustryORM
)


class FileMetadataRepository:
    """
    Repository for file metadata operations implementing TDD test behaviors.
    
    WHY: Provides database access that matches the validated test expectations
    CONTRIBUTION: Enables the file upload workflow to use structured metadata storage
    HOW: Implements CRUD operations with proper error handling and relationship management
    """
    
    def __init__(self):
        """
        Initialize repository with database session management.
        
        WHY: Ensures proper database connection lifecycle management
        CONTRIBUTION: Provides consistent database access patterns across the service
        HOW: Uses existing PostgressConnection configuration for session management
        """
        PostgressConnection.initialize()
        
    def _get_session(self) -> Session:
        """Get database session for operations."""
        return PostgressConnection.SessionLocal()

    def create_file_metadata(
        self, 
        filename: str,
        file_type: str,
        language: str,
        minio_bucket: str,
        minio_filename: str,
        original_content_type: str = None,
        file_size: int = None,
        qdrant_point_id: UUID = None
    ) -> FileMetadataORM:
        """
        Create base file metadata record - implements TDD Test Behavior 1.
        
        WHY: Satisfies test requirement for base file creation with constraint validation
        CONTRIBUTION: Provides the foundation for all file operations in the enhanced system
        HOW: Creates FileMetadataORM with validation that matches test constraints
        """
        session = self._get_session()
        try:
            file_metadata = FileMetadataORM(
                filename=filename,
                file_type=file_type,
                language=language,
                minio_bucket=minio_bucket,
                minio_filename=minio_filename,
                original_content_type=original_content_type,
                file_size=file_size,
                qdrant_point_id=qdrant_point_id
            )
            
            session.add(file_metadata)
            session.commit()
            session.refresh(file_metadata)
            return file_metadata
            
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"File metadata creation failed: {str(e)}")
        finally:
            session.close()

    def create_template_metadata(
        self,
        file_id: UUID,
        jobtype: str,
        industry_sectors: List[str] = None,
        template_subtype: str = "cover_letter",
        company_size_target: str = "any",
        effectiveness_score: float = 0.0
    ) -> TemplateMetadataORM:
        """
        Create template metadata - implements TDD Test Behavior 2.
        
        WHY: Satisfies test requirement for template metadata relationships with foreign key enforcement
        CONTRIBUTION: Enables template categorization and jobtype-based filtering
        HOW: Creates TemplateMetadataORM with proper foreign key relationship to FileMetadataORM
        """
        session = self._get_session()
        try:
            template_metadata = TemplateMetadataORM(
                file_id=file_id,
                jobtype=jobtype,
                industry_sectors=industry_sectors or [],
                template_subtype=template_subtype,
                company_size_target=company_size_target,
                effectiveness_score=effectiveness_score
            )
            
            session.add(template_metadata)
            session.commit()
            session.refresh(template_metadata)
            return template_metadata
            
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"Template metadata creation failed: {str(e)}")
        finally:
            session.close()

    def create_cv_metadata(
        self,
        file_id: UUID,
        primary_roles: List[str] = None,
        experience_years: int = None,
        industries_mentioned: List[str] = None,
        skills_extracted: List[str] = None,
        is_current_cv: bool = False,
        sections_extracted: Dict[str, Any] = None
    ) -> CVMetadataORM:
        """
        Create CV metadata with experience tracking.
        
        WHY: Supports CV-specific metadata for role matching and experience filtering
        CONTRIBUTION: Enables CV analysis and experience-based template recommendations
        HOW: Creates CVMetadataORM with proper validation and foreign key relationship
        """
        session = self._get_session()
        try:
            cv_metadata = CVMetadataORM(
                file_id=file_id,
                primary_roles=primary_roles or [],
                experience_years=experience_years,
                industries_mentioned=industries_mentioned or [],
                skills_extracted=skills_extracted or [],
                is_current_cv=is_current_cv,
                sections_extracted=sections_extracted or {},
                extraction_completed=True
            )
            
            session.add(cv_metadata)
            session.commit()
            session.refresh(cv_metadata)
            return cv_metadata
            
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"CV metadata creation failed: {str(e)}")
        finally:
            session.close()

    def get_by_minio_filename(self, bucket: str, filename: str) -> Optional[FileMetadataORM]:
        """
        Find file by MinIO bucket and filename - implements TDD Test Behavior 5.
        
        WHY: Provides efficient file lookup using the composite index from TDD tests
        CONTRIBUTION: Enables integration between MinIO storage and PostgreSQL metadata
        HOW: Uses the indexed minio_bucket + minio_filename lookup validated by performance tests
        """
        session = self._get_session()
        try:
            return session.query(FileMetadataORM).filter(
                FileMetadataORM.minio_bucket == bucket,
                FileMetadataORM.minio_filename == filename
            ).first()
        finally:
            session.close()

    def get_by_file_type_and_language(self, file_type: str, language: str) -> List[FileMetadataORM]:
        """
        Filter files by type and language - implements TDD Test Behavior 5.
        
        WHY: Provides efficient filtering using the composite index validated by TDD tests
        CONTRIBUTION: Enables frontend file filtering and categorization
        HOW: Uses the file_type + language composite index for optimal query performance
        """
        session = self._get_session()
        try:
            return session.query(FileMetadataORM).filter(
                FileMetadataORM.file_type == file_type,
                FileMetadataORM.language == language
            ).all()
        finally:
            session.close()

    def delete_by_id(self, file_id: UUID) -> bool:
        """
        Delete file metadata with cascade - implements TDD Test Behavior 3.
        
        WHY: Satisfies test requirement for cascade delete operations
        CONTRIBUTION: Ensures clean file removal without orphaned metadata records
        HOW: Deletes FileMetadataORM which cascades to template_metadata and cv_metadata
        """
        session = self._get_session()
        try:
            file_metadata = session.query(FileMetadataORM).filter(
                FileMetadataORM.id == file_id
            ).first()
            
            if not file_metadata:
                return False
                
            session.delete(file_metadata)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise ValueError(f"File deletion failed: {str(e)}")
        finally:
            session.close()

    def get_active_jobtypes(self) -> List[JobtypeORM]:
        """
        Get active jobtypes - implements TDD Test Behavior 4.
        
        WHY: Satisfies test requirement for jobtype uniqueness and active state management
        CONTRIBUTION: Provides dropdown data for frontend metadata collection
        HOW: Filters jobtypes by is_active=True using indexed query validated by tests
        """
        session = self._get_session()
        try:
            return session.query(JobtypeORM).filter(
                JobtypeORM.is_active == True
            ).order_by(JobtypeORM.name).all()
        finally:
            session.close()

    def get_active_industries(self) -> List[IndustryORM]:
        """
        Get active industries for multi-select dropdown.
        
        WHY: Provides industry vocabulary for template and CV categorization
        CONTRIBUTION: Enables industry-based filtering and categorization in frontend
        HOW: Filters industries by is_active=True with proper ordering
        """
        session = self._get_session()
        try:
            return session.query(IndustryORM).filter(
                IndustryORM.is_active == True
            ).order_by(IndustryORM.name).all()
        finally:
            session.close()

    def get_templates_by_jobtype(self, jobtype: str, language: str = None) -> List[FileMetadataORM]:
        """
        Get templates filtered by jobtype and optionally language.
        
        WHY: Enables jobtype-based template recommendations for cover letter generation
        CONTRIBUTION: Supports template filtering and recommendation engine features
        HOW: Joins FileMetadataORM with TemplateMetadataORM for efficient filtering
        """
        session = self._get_session()
        try:
            query = session.query(FileMetadataORM).join(TemplateMetadataORM).filter(
                FileMetadataORM.file_type == "template",
                TemplateMetadataORM.jobtype == jobtype
            )
            
            if language:
                query = query.filter(FileMetadataORM.language == language)
                
            return query.order_by(TemplateMetadataORM.effectiveness_score.desc()).all()
        finally:
            session.close()

    def get_current_cv(self) -> Optional[FileMetadataORM]:
        """
        Get the current CV marked as primary.
        
        WHY: Enables user workflow by identifying the most current CV version
        CONTRIBUTION: Supports CV management and cover letter context generation
        HOW: Uses indexed query on is_current_cv flag validated by TDD tests
        """
        session = self._get_session()
        try:
            return session.query(FileMetadataORM).join(CVMetadataORM).filter(
                CVMetadataORM.is_current_cv == True
            ).first()
        finally:
            session.close()