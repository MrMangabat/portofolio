# File: src/repositories/postgresql/CRUD_postgres.py
"""
PostgreSQL repository for corrections and job listings with standardized CRUD operations.

WHY: Provides a clean, consistent data access layer for correction and job listing management
CONTRIBUTION: Enables reliable database operations with proper error handling and transaction management
HOW: Uses SQLAlchemy ORM with session-per-operation pattern and comprehensive error handling
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from src.config.config_db_connections import PostgressConnection
from src.models.database.postgresql.postgres_models import (
    CorrectionORM, 
    CorrectionType, 
    JobListingORM, 
    JobListingItem
)


class CorrectionRepository:
    """
    Repository for correction operations with standardized CRUD pattern.
    
    WHY: Manages correction data (skills, words, sentences) for job application enhancement
    CONTRIBUTION: Provides consistent database access for correction management features
    HOW: Implements CRUD operations with proper session lifecycle and error handling
    """
    
    def __init__(self):
        """
        Initialize repository with database connection management.
        
        WHY: Ensures proper database connection lifecycle management
        CONTRIBUTION: Provides consistent database access patterns across the service
        HOW: Uses PostgressConnection for centralized session management
        """
        PostgressConnection.initialize()
        self.logger = logging.getLogger(__name__)
        
    def _get_session(self) -> Session:
        """
        Get database session for operations.
        
        WHY: Isolates each operation in its own transaction context
        CONTRIBUTION: Prevents session leaks and ensures proper resource cleanup
        HOW: Creates new session from configured SessionLocal factory
        """
        return PostgressConnection.SessionLocal()
    
    def get_all(self) -> List[CorrectionORM]:
        """
        Retrieve all corrections from database.
        
        WHY: Provides complete list of corrections for UI display and management
        CONTRIBUTION: Enables correction overview and bulk operations
        HOW: Queries all CorrectionORM records with proper session management
        """
        session = self._get_session()
        try:
            corrections = session.query(CorrectionORM).all()
            return corrections
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve corrections: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def get_by_type(self, correction_type: CorrectionType) -> List[CorrectionORM]:
        """
        Retrieve corrections filtered by type.
        
        WHY: Enables type-specific correction management (skills vs words vs sentences)
        CONTRIBUTION: Supports categorized display and type-specific operations
        HOW: Filters query by correction_type enum with proper type validation
        
        Args:
            correction_type: The type of corrections to retrieve (skill/word/sentence)
            
        Returns:
            List of corrections matching the specified type
        """
        session = self._get_session()
        try:
            corrections = session.query(CorrectionORM).filter(
                CorrectionORM.type == correction_type
            ).all()
            return corrections
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve corrections by type {correction_type}: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def get_by_id(self, correction_id: UUID) -> Optional[CorrectionORM]:
        """
        Retrieve single correction by ID.
        
        WHY: Enables targeted operations on specific corrections
        CONTRIBUTION: Supports update and delete operations with existence validation
        HOW: Queries by primary key with null-safe return
        
        Args:
            correction_id: UUID primary key of the correction
            
        Returns:
            CorrectionORM instance or None if not found
        """
        session = self._get_session()
        try:
            correction = session.query(CorrectionORM).filter(
                CorrectionORM.id == correction_id
            ).first()
            return correction
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve correction {correction_id}: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def create(self, text: str, correction_type: CorrectionType) -> CorrectionORM:
        """
        Create new correction record.
        
        WHY: Allows users to add new corrections to improve job application quality
        CONTRIBUTION: Expands the correction database for better text enhancement
        HOW: Creates CorrectionORM with validation and returns persisted entity
        
        Args:
            text: The correction text content
            correction_type: Type classification (skill/word/sentence)
            
        Returns:
            Created CorrectionORM with generated ID
            
        Raises:
            ValueError: If creation fails due to constraints or validation
        """
        session = self._get_session()
        try:
            correction = CorrectionORM(text=text, type=correction_type)
            
            session.add(correction)
            session.commit()
            session.refresh(correction)
            
            self.logger.info(f"Created correction {correction.id} of type {correction_type}")
            return correction
            
        except IntegrityError as e:
            session.rollback()
            self.logger.error(f"Integrity error creating correction: {str(e)}")
            raise ValueError(f"Correction creation failed - possible duplicate: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error creating correction: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def update(self, correction_id: UUID, text: str = None, correction_type: CorrectionType = None) -> Optional[CorrectionORM]:
        """
        Update existing correction.
        
        WHY: Enables correction refinement based on user feedback
        CONTRIBUTION: Maintains correction quality and relevance over time
        HOW: Updates specified fields with null-safe partial updates
        
        Args:
            correction_id: ID of correction to update
            text: New text content (optional)
            correction_type: New type classification (optional)
            
        Returns:
            Updated CorrectionORM or None if not found
        """
        session = self._get_session()
        try:
            correction = session.query(CorrectionORM).filter(
                CorrectionORM.id == correction_id
            ).first()
            
            if not correction:
                self.logger.warning(f"Correction {correction_id} not found for update")
                return None
            
            if text is not None:
                correction.text = text
            if correction_type is not None:
                correction.type = correction_type
            
            session.commit()
            session.refresh(correction)
            
            self.logger.info(f"Updated correction {correction_id}")
            return correction
            
        except IntegrityError as e:
            session.rollback()
            self.logger.error(f"Integrity error updating correction {correction_id}: {str(e)}")
            raise ValueError(f"Update failed - constraint violation: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error updating correction {correction_id}: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def delete(self, correction_id: UUID) -> bool:
        """
        Delete correction by ID.
        
        WHY: Removes outdated or incorrect corrections from the system
        CONTRIBUTION: Maintains correction database quality and relevance
        HOW: Performs hard delete with existence check and success confirmation
        
        Args:
            correction_id: ID of correction to delete
            
        Returns:
            True if deleted, False if not found
        """
        session = self._get_session()
        try:
            correction = session.query(CorrectionORM).filter(
                CorrectionORM.id == correction_id
            ).first()
            
            if not correction:
                self.logger.warning(f"Correction {correction_id} not found for deletion")
                return False
            
            session.delete(correction)
            session.commit()
            
            self.logger.info(f"Deleted correction {correction_id}")
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Failed to delete correction {correction_id}: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def bulk_create(self, corrections: List[Dict[str, Any]]) -> List[CorrectionORM]:
        """
        Create multiple corrections in a single transaction.
        
        WHY: Enables efficient batch import of corrections
        CONTRIBUTION: Supports bulk data loading and migration scenarios
        HOW: Uses single transaction for all inserts with rollback on any failure
        
        Args:
            corrections: List of dicts with 'text' and 'type' keys
            
        Returns:
            List of created CorrectionORM instances
            
        Raises:
            ValueError: If any creation fails, entire batch is rolled back
        """
        session = self._get_session()
        try:
            created_corrections = []
            
            for correction_data in corrections:
                correction = CorrectionORM(
                    text=correction_data['text'],
                    type=correction_data['type']
                )
                session.add(correction)
                created_corrections.append(correction)
            
            session.commit()
            
            # Refresh all objects to get generated IDs
            for correction in created_corrections:
                session.refresh(correction)
            
            self.logger.info(f"Bulk created {len(created_corrections)} corrections")
            return created_corrections
            
        except (IntegrityError, SQLAlchemyError) as e:
            session.rollback()
            self.logger.error(f"Failed to bulk create corrections: {str(e)}")
            raise ValueError(f"Bulk creation failed: {str(e)}")
        finally:
            session.close()


class JobListingRepository:
    """
    Repository for job listing operations with standardized CRUD pattern.
    
    WHY: Manages job listing data for application tracking and analysis
    CONTRIBUTION: Provides reliable storage for job opportunities and application history
    HOW: Implements CRUD operations with proper model serialization and error handling
    """
    
    def __init__(self):
        """
        Initialize repository with database connection management.
        
        WHY: Ensures proper database connection lifecycle management
        CONTRIBUTION: Provides consistent database access patterns across the service
        HOW: Uses PostgressConnection for centralized session management
        """
        PostgressConnection.initialize()
        self.logger = logging.getLogger(__name__)
        
    def _get_session(self) -> Session:
        """
        Get database session for operations.
        
        WHY: Isolates each operation in its own transaction context
        CONTRIBUTION: Prevents session leaks and ensures proper resource cleanup
        HOW: Creates new session from configured SessionLocal factory
        """
        return PostgressConnection.SessionLocal()
    
    def get_all(self) -> List[JobListingORM]:
        """
        Retrieve all job listings from database.
        
        WHY: Provides complete job listing overview for tracking and analysis
        CONTRIBUTION: Enables job search history and application management
        HOW: Queries all JobListingORM records with proper session management
        """
        session = self._get_session()
        try:
            job_listings = session.query(JobListingORM).all()
            return job_listings
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve job listings: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def get_by_id(self, job_listing_id: UUID) -> Optional[JobListingORM]:
        """
        Retrieve single job listing by ID.
        
        WHY: Enables targeted operations on specific job listings
        CONTRIBUTION: Supports detailed view and update operations
        HOW: Queries by primary key with null-safe return
        
        Args:
            job_listing_id: UUID primary key of the job listing
            
        Returns:
            JobListingORM instance or None if not found
        """
        session = self._get_session()
        try:
            job_listing = session.query(JobListingORM).filter(
                JobListingORM.id == job_listing_id
            ).first()
            return job_listing
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to retrieve job listing {job_listing_id}: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def create(self, job_listing_data: JobListingItem) -> JobListingORM:
        """
        Create new job listing record.
        
        WHY: Stores new job opportunities for tracking and application
        CONTRIBUTION: Builds comprehensive job application history
        HOW: Converts Pydantic model to ORM with proper validation
        
        Args:
            job_listing_data: Pydantic model with job listing details
            
        Returns:
            Created JobListingORM with generated ID
            
        Raises:
            ValueError: If creation fails due to constraints or validation
        """
        session = self._get_session()
        try:
            # Convert Pydantic model to ORM
            job_listing = JobListingORM(**job_listing_data.model_dump())
            
            session.add(job_listing)
            session.commit()
            session.refresh(job_listing)
            
            self.logger.info(f"Created job listing {job_listing.id}")
            return job_listing
            
        except IntegrityError as e:
            session.rollback()
            self.logger.error(f"Integrity error creating job listing: {str(e)}")
            raise ValueError(f"Job listing creation failed - possible duplicate: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error creating job listing: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def update(self, job_listing_id: UUID, update_data: Dict[str, Any]) -> Optional[JobListingORM]:
        """
        Update existing job listing.
        
        WHY: Allows updating job status, notes, or application progress
        CONTRIBUTION: Maintains accurate job application tracking
        HOW: Updates specified fields with dictionary-based partial updates
        
        Args:
            job_listing_id: ID of job listing to update
            update_data: Dictionary of fields to update
            
        Returns:
            Updated JobListingORM or None if not found
        """
        session = self._get_session()
        try:
            job_listing = session.query(JobListingORM).filter(
                JobListingORM.id == job_listing_id
            ).first()
            
            if not job_listing:
                self.logger.warning(f"Job listing {job_listing_id} not found for update")
                return None
            
            # Update fields from dictionary
            for key, value in update_data.items():
                if hasattr(job_listing, key):
                    setattr(job_listing, key, value)
            
            session.commit()
            session.refresh(job_listing)
            
            self.logger.info(f"Updated job listing {job_listing_id}")
            return job_listing
            
        except IntegrityError as e:
            session.rollback()
            self.logger.error(f"Integrity error updating job listing {job_listing_id}: {str(e)}")
            raise ValueError(f"Update failed - constraint violation: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error updating job listing {job_listing_id}: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def delete(self, job_listing_id: UUID) -> bool:
        """
        Delete job listing by ID.
        
        WHY: Removes outdated or cancelled job listings
        CONTRIBUTION: Maintains clean job listing database
        HOW: Performs hard delete with existence check and success confirmation
        
        Args:
            job_listing_id: ID of job listing to delete
            
        Returns:
            True if deleted, False if not found
        """
        session = self._get_session()
        try:
            job_listing = session.query(JobListingORM).filter(
                JobListingORM.id == job_listing_id
            ).first()
            
            if not job_listing:
                self.logger.warning(f"Job listing {job_listing_id} not found for deletion")
                return False
            
            session.delete(job_listing)
            session.commit()
            
            self.logger.info(f"Deleted job listing {job_listing_id}")
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Failed to delete job listing {job_listing_id}: {str(e)}")
            raise ValueError(f"Database operation failed: {str(e)}")
        finally:
            session.close()
    
    def search(self, **filters) -> List[JobListingORM]:
        """
        Search job listings with flexible filtering.
        
        WHY: Enables advanced job search and filtering capabilities
        CONTRIBUTION: Supports complex queries for job discovery
        HOW: Builds dynamic query based on provided filter parameters
        
        Args:
            **filters: Keyword arguments for filtering (e.g., company="Google", location="NYC")
            
        Returns:
            List of JobListingORM matching the filters
        """
        session = self._get_session()
        try:
            query = session.query(JobListingORM)
            
            # Apply filters dynamically
            for key, value in filters.items():
                if hasattr(JobListingORM, key) and value is not None:
                    query = query.filter(getattr(JobListingORM, key) == value)
            
            job_listings = query.all()
            return job_listings
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to search job listings with filters {filters}: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()
    
    def count(self, **filters) -> int:
        """
        Count job listings matching filters.
        
        WHY: Provides statistics without fetching full records
        CONTRIBUTION: Enables efficient dashboard metrics and pagination
        HOW: Uses COUNT query with optional filtering
        
        Args:
            **filters: Optional keyword arguments for filtering
            
        Returns:
            Count of matching job listings
        """
        session = self._get_session()
        try:
            query = session.query(JobListingORM)
            
            # Apply filters if provided
            for key, value in filters.items():
                if hasattr(JobListingORM, key) and value is not None:
                    query = query.filter(getattr(JobListingORM, key) == value)
            
            count = query.count()
            return count
            
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to count job listings: {str(e)}")
            raise ValueError(f"Database query failed: {str(e)}")
        finally:
            session.close()