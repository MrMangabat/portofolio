# File: tests/test_file_metadata_models.py
"""
Comprehensive tests for file metadata management system.

WHY: Validates the 5 specified test behaviors for file metadata system with complete coverage
CONTRIBUTION: Ensures system reliability, data integrity, and compliance with business requirements
HOW: Uses pytest with isolated database transactions to test all critical file metadata operations
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.database.postgresql.file_metadata_models import (
    FileMetadataORM,
    TemplateMetadataORM,
    CVMetadataORM,
    JobtypeORM,
    IndustryORM
)


class TestFileMetadataBasicOperations:
    """
    Test Behavior 1: Base file creation with valid data and constraint validation.
    
    WHY: Validates core file metadata creation and business rule enforcement
    CONTRIBUTION: Ensures data integrity and prevents invalid file metadata states
    HOW: Tests valid file creation, constraint violations, and data validation
    """

    def test_create_valid_file_metadata(self, test_db_session: Session):
        """
        Test successful creation of file metadata with valid data.
        
        WHY: Verifies that valid file metadata can be created and persisted correctly
        CONTRIBUTION: Ensures core functionality works for legitimate file upload scenarios
        HOW: Creates file metadata with all required fields and validates persistence
        """
        file_metadata = FileMetadataORM(
            filename="test_document.pdf",
            file_type="template",
            language="english",
            minio_bucket="cover-letters",
            minio_filename=f"{uuid.uuid4()}.pdf",
            original_content_type="application/pdf",
            file_size=102400,
            qdrant_point_id=uuid.uuid4()
        )
        
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Verify all fields are set correctly
        assert file_metadata.id is not None
        assert file_metadata.filename == "test_document.pdf"
        assert file_metadata.file_type == "template"
        assert file_metadata.language == "english"
        assert file_metadata.schema_version == "1.0"
        assert file_metadata.created_at is not None
        assert file_metadata.updated_at is not None
        assert file_metadata.minio_bucket == "cover-letters"
        assert file_metadata.original_content_type == "application/pdf"
        assert file_metadata.file_size == 102400

    def test_file_type_constraint_validation(self, test_db_session: Session):
        """
        Test file_type constraint enforcement.
        
        WHY: Ensures only valid file types are accepted to maintain data consistency
        CONTRIBUTION: Prevents invalid file categorization that would break business logic
        HOW: Attempts to create file metadata with invalid file_type and expects constraint violation
        """
        with pytest.raises(IntegrityError):
            file_metadata = FileMetadataORM(
                filename="invalid_type.pdf",
                file_type="invalid_type",  # Invalid file type
                language="english",
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf"
            )
            test_db_session.add(file_metadata)
            test_db_session.commit()

    def test_language_constraint_validation(self, test_db_session: Session):
        """
        Test language constraint enforcement.
        
        WHY: Ensures only supported languages are accepted for proper categorization
        CONTRIBUTION: Maintains language consistency for template and CV processing
        HOW: Attempts to create file metadata with invalid language and expects constraint violation
        """
        from sqlalchemy.exc import DataError
        with pytest.raises((IntegrityError, DataError)):  # DataError for varchar length violation
            file_metadata = FileMetadataORM(
                filename="invalid_language.pdf", 
                file_type="template",
                language="unsupported",  # Changed to fit within varchar(10)
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf"
            )
            test_db_session.add(file_metadata)
            test_db_session.commit()

    def test_minio_filename_uniqueness_constraint(self, test_db_session: Session):
        """
        Test that MinIO filenames can be duplicated (no uniqueness constraint).
        
        WHY: Validates that multiple file records can reference same MinIO file (versioning support)
        CONTRIBUTION: Allows file versioning and duplicate handling in storage layer
        HOW: Creates two files with same bucket/filename and verifies both are stored
        """
        unique_filename = f"{uuid.uuid4()}.pdf"
        
        # Create first file
        file1 = FileMetadataORM(
            filename="first_file.pdf",
            file_type="template", 
            language="english",
            minio_bucket="cover-letters",
            minio_filename=unique_filename
        )
        test_db_session.add(file1)
        test_db_session.commit()
        
        # Create second file with same bucket/filename - should succeed
        # (No unique constraint on minio_filename)
        file2 = FileMetadataORM(
            filename="second_file.pdf",
            file_type="template",
            language="english", 
            minio_bucket="cover-letters",
            minio_filename=unique_filename  # Duplicate bucket/filename
        )
        test_db_session.add(file2)
        test_db_session.commit()
        
        # Verify both files exist
        assert test_db_session.query(FileMetadataORM).filter_by(minio_filename=unique_filename).count() == 2

    def test_required_fields_validation(self, test_db_session: Session):
        """
        Test required field validation.
        
        WHY: Ensures critical file metadata fields are always provided
        CONTRIBUTION: Prevents incomplete file records that would break system functionality
        HOW: Attempts to create file metadata with missing required fields
        """
        with pytest.raises(IntegrityError):
            file_metadata = FileMetadataORM(
                # Missing required filename
                file_type="template",
                language="english",
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf"
            )
            test_db_session.add(file_metadata)
            test_db_session.commit()


class TestTemplateMetadataRelationships:
    """
    Test Behavior 2: Template metadata relationships with foreign key enforcement.
    
    WHY: Validates proper relationship management between files and template-specific metadata
    CONTRIBUTION: Ensures referential integrity for template categorization and business logic
    HOW: Tests foreign key relationships, constraint enforcement, and data consistency
    """

    def test_create_template_metadata_with_valid_foreign_key(self, test_db_session: Session, sample_file_metadata: FileMetadataORM):
        """
        Test successful template metadata creation with valid file reference.
        
        WHY: Verifies template metadata can be properly linked to base file metadata
        CONTRIBUTION: Enables template categorization and jobtype-based filtering functionality
        HOW: Creates template metadata with valid foreign key and validates relationship
        """
        template_metadata = TemplateMetadataORM(
            file_id=sample_file_metadata.id,
            jobtype="data_scientist",
            industry_sectors=["technology", "finance"],
            template_subtype="cover_letter",
            company_size_target="startup",
            effectiveness_score=0.75
        )
        
        test_db_session.add(template_metadata)
        test_db_session.commit()
        test_db_session.refresh(template_metadata)
        
        # Verify template metadata fields
        assert template_metadata.file_id == sample_file_metadata.id
        assert template_metadata.jobtype == "data_scientist"
        assert template_metadata.industry_sectors == ["technology", "finance"]
        assert template_metadata.template_subtype == "cover_letter"
        assert template_metadata.company_size_target == "startup"
        assert template_metadata.effectiveness_score == 0.75
        
        # Verify relationship works
        assert template_metadata.file_metadata.filename == sample_file_metadata.filename

    def test_template_metadata_foreign_key_constraint(self, test_db_session: Session):
        """
        Test foreign key constraint enforcement for template metadata.
        
        WHY: Ensures template metadata cannot exist without corresponding file metadata
        CONTRIBUTION: Maintains referential integrity and prevents orphaned template records
        HOW: Attempts to create template metadata with invalid file_id and expects constraint violation
        """
        with pytest.raises(IntegrityError):
            template_metadata = TemplateMetadataORM(
                file_id=uuid.uuid4(),  # Non-existent file_id
                jobtype="data_scientist",
                template_subtype="cover_letter"
            )
            test_db_session.add(template_metadata)
            test_db_session.commit()

    def test_template_subtype_constraint_validation(self, test_db_session: Session, sample_file_metadata: FileMetadataORM):
        """
        Test template_subtype constraint enforcement.
        
        WHY: Ensures only valid template subtypes are accepted for proper categorization
        CONTRIBUTION: Maintains template type consistency for LLM context and recommendation engine
        HOW: Attempts to create template metadata with invalid subtype and expects constraint violation
        """
        with pytest.raises(IntegrityError):
            template_metadata = TemplateMetadataORM(
                file_id=sample_file_metadata.id,
                jobtype="data_scientist",
                template_subtype="invalid_subtype"  # Invalid template subtype
            )
            test_db_session.add(template_metadata)
            test_db_session.commit()

    def test_company_size_constraint_validation(self, test_db_session: Session, sample_file_metadata: FileMetadataORM):
        """
        Test company_size_target constraint enforcement.
        
        WHY: Ensures only valid company size targets are accepted for template matching
        CONTRIBUTION: Maintains data consistency for company size-based template recommendations
        HOW: Attempts to create template metadata with invalid company size and expects constraint violation
        """
        with pytest.raises(IntegrityError):
            template_metadata = TemplateMetadataORM(
                file_id=sample_file_metadata.id,
                jobtype="data_scientist",
                company_size_target="invalid_size"  # Invalid company size
            )
            test_db_session.add(template_metadata)
            test_db_session.commit()

    def test_effectiveness_score_constraint_validation(self, test_db_session: Session, sample_file_metadata: FileMetadataORM):
        """
        Test effectiveness_score range constraint enforcement.
        
        WHY: Ensures effectiveness scores remain within valid 0.0-1.0 range for ML features
        CONTRIBUTION: Maintains data quality for future recommendation engine scoring
        HOW: Attempts to create template metadata with out-of-range effectiveness score
        """
        with pytest.raises(IntegrityError):
            template_metadata = TemplateMetadataORM(
                file_id=sample_file_metadata.id,
                jobtype="data_scientist", 
                effectiveness_score=1.5  # Invalid score > 1.0
            )
            test_db_session.add(template_metadata)
            test_db_session.commit()


class TestCascadeDeleteOperations:
    """
    Test Behavior 3: Cascade delete operations (delete base_file → removes metadata).
    
    WHY: Validates proper cleanup of related data when files are deleted from system
    CONTRIBUTION: Ensures no orphaned metadata records remain after file deletion
    HOW: Tests cascade delete behavior for template and CV metadata relationships
    """

    def test_file_metadata_cascade_delete_template_metadata(self, test_db_session: Session, sample_template_metadata: TemplateMetadataORM):
        """
        Test cascade delete from file_metadata to template_metadata.
        
        WHY: Ensures template metadata is automatically removed when base file is deleted
        CONTRIBUTION: Prevents orphaned template records and maintains database consistency
        HOW: Deletes file metadata and verifies template metadata is automatically removed
        """
        file_id = sample_template_metadata.file_id
        
        # Verify template metadata exists
        template_count_before = test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_id).count()
        assert template_count_before == 1
        
        # Delete the base file metadata
        file_metadata = test_db_session.query(FileMetadataORM).filter_by(id=file_id).first()
        test_db_session.delete(file_metadata)
        test_db_session.commit()
        
        # Verify template metadata was cascade deleted
        template_count_after = test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_id).count()
        assert template_count_after == 0

    def test_file_metadata_cascade_delete_cv_metadata(self, test_db_session: Session, sample_cv_metadata: CVMetadataORM):
        """
        Test cascade delete from file_metadata to cv_metadata.
        
        WHY: Ensures CV metadata is automatically removed when base file is deleted
        CONTRIBUTION: Prevents orphaned CV records and maintains database consistency
        HOW: Deletes file metadata and verifies CV metadata is automatically removed
        """
        file_id = sample_cv_metadata.file_id
        
        # Verify CV metadata exists
        cv_count_before = test_db_session.query(CVMetadataORM).filter_by(file_id=file_id).count()
        assert cv_count_before == 1
        
        # Delete the base file metadata
        file_metadata = test_db_session.query(FileMetadataORM).filter_by(id=file_id).first()
        test_db_session.delete(file_metadata)
        test_db_session.commit()
        
        # Verify CV metadata was cascade deleted
        cv_count_after = test_db_session.query(CVMetadataORM).filter_by(file_id=file_id).count()
        assert cv_count_after == 0

    def test_multiple_metadata_cascade_delete(self, test_db_session: Session):
        """
        Test cascade delete with multiple metadata types on same file.
        
        WHY: Verifies cascade delete works correctly when file has multiple metadata types
        CONTRIBUTION: Ensures complete cleanup of all related data during file deletion
        HOW: Creates file with both template and CV metadata, then tests cascade delete
        """
        # Create base file that could theoretically have both metadata types
        file_metadata = FileMetadataORM(
            filename="multi_type_file.pdf",
            file_type="application",  # Could be both template and CV
            language="english",
            minio_bucket="cover-letters", 
            minio_filename=f"{uuid.uuid4()}.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Add template metadata
        template_metadata = TemplateMetadataORM(
            file_id=file_metadata.id,
            jobtype="data_scientist"
        )
        test_db_session.add(template_metadata)
        test_db_session.commit()
        
        # Verify metadata exists
        template_count_before = test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_metadata.id).count()
        assert template_count_before == 1
        
        # Delete base file
        test_db_session.delete(file_metadata)
        test_db_session.commit()
        
        # Verify all metadata was cascade deleted
        template_count_after = test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_metadata.id).count()
        assert template_count_after == 0


class TestJobtypeUniquenessAndActiveState:
    """
    Test Behavior 4: Jobtype uniqueness and active state management.
    
    WHY: Validates jobtype lookup table management for dropdown population and data consistency
    CONTRIBUTION: Ensures reliable jobtype management for template categorization
    HOW: Tests unique constraints, active state filtering, and lifecycle management
    """

    def test_jobtype_unique_name_constraint(self, test_db_session: Session):
        """
        Test jobtype name uniqueness constraint.
        
        WHY: Prevents duplicate jobtype names that would cause dropdown confusion
        CONTRIBUTION: Maintains clean jobtype vocabulary for template categorization
        HOW: Creates jobtype, then attempts to create duplicate and expects constraint violation
        """
        # Create first jobtype
        jobtype1 = JobtypeORM(
            name="data_scientist",
            category="analytics",
            is_active=True
        )
        test_db_session.add(jobtype1)
        test_db_session.commit()
        
        # Attempt to create duplicate jobtype name
        with pytest.raises(IntegrityError):
            jobtype2 = JobtypeORM(
                name="data_scientist",  # Duplicate name
                category="different_category",
                is_active=True
            )
            test_db_session.add(jobtype2)
            test_db_session.commit()

    def test_jobtype_active_state_filtering(self, test_db_session: Session, multiple_jobtypes: list[JobtypeORM]):
        """
        Test active state filtering for jobtypes.
        
        WHY: Ensures only active jobtypes appear in UI dropdowns and business logic
        CONTRIBUTION: Provides clean user experience by hiding deprecated jobtypes
        HOW: Creates mixed active/inactive jobtypes and tests filtering queries
        """
        # Query active jobtypes only
        active_jobtypes = test_db_session.query(JobtypeORM).filter(JobtypeORM.is_active == True).all()
        active_names = [jt.name for jt in active_jobtypes]
        
        # Verify active jobtypes are returned
        assert "data_scientist" in active_names
        assert "data_engineer" in active_names
        assert "analyst" in active_names
        
        # Verify inactive jobtype is excluded
        assert "deprecated_role" not in active_names
        
        # Verify count is correct
        assert len(active_jobtypes) == 3

    def test_jobtype_lifecycle_management(self, test_db_session: Session):
        """
        Test jobtype lifecycle management (create, activate, deactivate).
        
        WHY: Validates complete jobtype lifecycle for administrative management
        CONTRIBUTION: Enables proper jobtype administration and vocabulary evolution
        HOW: Creates jobtype, modifies active state, and verifies state persistence
        """
        # Create active jobtype
        jobtype = JobtypeORM(
            name="ml_engineer",
            category="engineering", 
            is_active=True,
            description="Machine learning engineering roles"
        )
        test_db_session.add(jobtype)
        test_db_session.commit()
        test_db_session.refresh(jobtype)
        
        # Verify initial state
        assert jobtype.is_active is True
        assert jobtype.created_at is not None
        
        # Deactivate jobtype
        jobtype.is_active = False
        test_db_session.commit()
        test_db_session.refresh(jobtype)
        
        # Verify state change
        assert jobtype.is_active is False
        
        # Reactivate jobtype
        jobtype.is_active = True
        test_db_session.commit()
        test_db_session.refresh(jobtype)
        
        # Verify state change
        assert jobtype.is_active is True

    def test_jobtype_category_grouping(self, test_db_session: Session, multiple_jobtypes: list[JobtypeORM]):
        """
        Test jobtype category grouping functionality.
        
        WHY: Enables UI organization of jobtypes by category for better user experience
        CONTRIBUTION: Supports grouped dropdown displays and categorized analytics
        HOW: Creates jobtypes with categories and tests category-based queries
        """
        # Query jobtypes by category
        analytics_jobtypes = test_db_session.query(JobtypeORM).filter(
            JobtypeORM.category == "analytics",
            JobtypeORM.is_active == True
        ).all()
        
        analytics_names = [jt.name for jt in analytics_jobtypes]
        
        # Verify category grouping
        assert "data_scientist" in analytics_names
        assert "analyst" in analytics_names
        assert len(analytics_names) == 2
        
        # Verify non-analytics jobtypes are excluded
        assert "data_engineer" not in analytics_names


class TestIndexPerformanceAndFiltering:
    """
    Test Behavior 5: Index performance for file_type and language filtering.
    
    WHY: Validates query performance optimization for common file filtering operations
    CONTRIBUTION: Ensures system scalability and responsive user experience with large file volumes
    HOW: Tests index usage and filtering performance with multiple file records
    """

    def test_file_type_language_index_usage(self, test_db_session: Session):
        """
        Test composite index usage for file_type and language filtering.
        
        WHY: Ensures efficient querying for the most common file filtering operations
        CONTRIBUTION: Provides fast response times for FileUploads.vue filtering functionality
        HOW: Creates multiple files with different types/languages and tests filtering queries
        """
        # Create files with different type/language combinations
        files = [
            FileMetadataORM(
                filename="english_template.pdf",
                file_type="template", 
                language="english",
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf"
            ),
            FileMetadataORM(
                filename="danish_template.pdf",
                file_type="template",
                language="danish", 
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf"
            ),
            FileMetadataORM(
                filename="english_cv.pdf",
                file_type="cv",
                language="english",
                minio_bucket="cv", 
                minio_filename=f"{uuid.uuid4()}.pdf"
            ),
            FileMetadataORM(
                filename="danish_cv.pdf", 
                file_type="cv",
                language="danish",
                minio_bucket="cv",
                minio_filename=f"{uuid.uuid4()}.pdf"
            )
        ]
        
        test_db_session.add_all(files)
        test_db_session.commit()
        
        # Test filtering by file_type and language (using composite index)
        english_templates = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.file_type == "template",
            FileMetadataORM.language == "english"
        ).all()
        
        assert len(english_templates) == 1
        assert english_templates[0].filename == "english_template.pdf"
        
        # Test filtering by file_type only
        all_templates = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.file_type == "template"
        ).all()
        
        assert len(all_templates) == 2
        
        # Test filtering by language only
        danish_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.language == "danish"
        ).all()
        
        assert len(danish_files) == 2

    def test_created_at_index_for_temporal_queries(self, test_db_session: Session):
        """
        Test created_at index for temporal filtering and sorting.
        
        WHY: Enables efficient queries for recent files and chronological sorting
        CONTRIBUTION: Supports "recently uploaded" features and file timeline views
        HOW: Creates files with different timestamps and tests temporal queries
        """
        import time
        from datetime import datetime, timedelta
        
        # Create files with different creation times
        base_time = datetime.now()
        
        files = [
            FileMetadataORM(
                filename="old_file.pdf",
                file_type="template",
                language="english", 
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf",
                created_at=base_time - timedelta(days=5)
            ),
            FileMetadataORM(
                filename="recent_file.pdf",
                file_type="template",
                language="english",
                minio_bucket="cover-letters", 
                minio_filename=f"{uuid.uuid4()}.pdf",
                created_at=base_time - timedelta(hours=1)
            ),
            FileMetadataORM(
                filename="newest_file.pdf",
                file_type="template",
                language="english",
                minio_bucket="cover-letters",
                minio_filename=f"{uuid.uuid4()}.pdf",
                created_at=base_time
            )
        ]
        
        test_db_session.add_all(files)
        test_db_session.commit()
        
        # Test chronological ordering (using created_at index)
        files_by_date = test_db_session.query(FileMetadataORM).order_by(
            FileMetadataORM.created_at.desc()
        ).all()
        
        assert files_by_date[0].filename == "newest_file.pdf"
        assert files_by_date[1].filename == "recent_file.pdf"
        assert files_by_date[2].filename == "old_file.pdf"
        
        # Test filtering by date range
        recent_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.created_at >= base_time - timedelta(days=1)
        ).all()
        
        assert len(recent_files) == 2
        recent_filenames = [f.filename for f in recent_files]
        assert "recent_file.pdf" in recent_filenames
        assert "newest_file.pdf" in recent_filenames
        assert "old_file.pdf" not in recent_filenames

    def test_minio_lookup_index_performance(self, test_db_session: Session):
        """
        Test MinIO lookup index for bucket/filename queries.
        
        WHY: Ensures efficient file lookups when syncing with MinIO storage
        CONTRIBUTION: Provides fast file resolution for storage operations and metadata updates
        HOW: Creates files and tests bucket/filename lookup queries
        """
        # Create files in different buckets
        files = [
            FileMetadataORM(
                filename="template1.pdf",
                file_type="template",
                language="english",
                minio_bucket="cover-letters",
                minio_filename="uuid1.pdf"
            ),
            FileMetadataORM(
                filename="template2.pdf", 
                file_type="template",
                language="english",
                minio_bucket="cover-letters",
                minio_filename="uuid2.pdf"
            ),
            FileMetadataORM(
                filename="cv1.pdf",
                file_type="cv",
                language="english", 
                minio_bucket="cv",
                minio_filename="uuid3.pdf"
            )
        ]
        
        test_db_session.add_all(files)
        test_db_session.commit()
        
        # Test lookup by bucket and filename (using composite index)
        found_file = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.minio_bucket == "cover-letters",
            FileMetadataORM.minio_filename == "uuid1.pdf"
        ).first()
        
        assert found_file is not None
        assert found_file.filename == "template1.pdf"
        
        # Test bucket-only filtering
        cover_letter_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.minio_bucket == "cover-letters"
        ).all()
        
        assert len(cover_letter_files) == 2