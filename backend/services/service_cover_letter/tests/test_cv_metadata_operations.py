# File: tests/test_cv_metadata_operations.py
"""
Specialized tests for CV metadata operations and business logic.

WHY: Provides focused testing for CV-specific functionality and edge cases
CONTRIBUTION: Ensures complete test coverage for CV processing features and SonarCube compliance
HOW: Tests CV metadata validation, extraction status tracking, and experience calculations
"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.database.postgresql.file_metadata_models import (
    FileMetadataORM,
    CVMetadataORM
)


class TestCVMetadataValidation:
    """
    Test CV metadata validation and constraint enforcement.
    
    WHY: Validates CV-specific business rules and data integrity constraints
    CONTRIBUTION: Ensures reliable CV processing and prevents invalid CV metadata states
    HOW: Tests experience range validation, extraction status management, and JSON field handling
    """

    def test_experience_years_valid_range(self, test_db_session: Session):
        """
        Test valid experience years range (0-50).
        
        WHY: Ensures experience values are realistic for business logic and user experience
        CONTRIBUTION: Prevents invalid experience data that would break CV matching algorithms
        HOW: Creates CV metadata with boundary values and validates acceptance
        """
        # Create base file
        file_metadata = FileMetadataORM(
            filename="test_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv",
            minio_filename="test-cv.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Test minimum valid experience (0 years)
        cv_metadata_min = CVMetadataORM(
            file_id=file_metadata.id,
            experience_years=0
        )
        test_db_session.add(cv_metadata_min)
        test_db_session.commit()
        
        assert cv_metadata_min.experience_years == 0
        
        # Test maximum valid experience (50 years)
        test_db_session.delete(cv_metadata_min)
        test_db_session.commit()
        
        cv_metadata_max = CVMetadataORM(
            file_id=file_metadata.id,
            experience_years=50
        )
        test_db_session.add(cv_metadata_max)
        test_db_session.commit()
        
        assert cv_metadata_max.experience_years == 50

    def test_experience_years_invalid_range(self, test_db_session: Session):
        """
        Test experience years constraint violation.
        
        WHY: Prevents unrealistic experience values that would cause system errors
        CONTRIBUTION: Maintains data quality for CV matching and experience-based filtering
        HOW: Attempts to create CV metadata with out-of-range experience values
        """
        # Create base file
        file_metadata = FileMetadataORM(
            filename="invalid_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv", 
            minio_filename="invalid-cv.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Test negative experience years
        with pytest.raises(IntegrityError):
            cv_metadata_negative = CVMetadataORM(
                file_id=file_metadata.id,
                experience_years=-1  # Invalid negative experience
            )
            test_db_session.add(cv_metadata_negative)
            test_db_session.commit()
        
        # Rollback the failed transaction
        test_db_session.rollback()
        
        # Test excessive experience years
        with pytest.raises(IntegrityError):
            cv_metadata_excessive = CVMetadataORM(
                file_id=file_metadata.id,
                experience_years=51  # Invalid excessive experience
            )
            test_db_session.add(cv_metadata_excessive)
            test_db_session.commit()
        
        # Rollback the failed transaction
        test_db_session.rollback()

    def test_json_field_default_values(self, test_db_session: Session):
        """
        Test JSON field default values and structure.
        
        WHY: Ensures JSON fields have proper default structures for consistent processing
        CONTRIBUTION: Prevents null pointer errors and provides predictable data structures
        HOW: Creates CV metadata without explicit JSON values and validates defaults
        """
        # Create base file
        file_metadata = FileMetadataORM(
            filename="default_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv",
            minio_filename="default-cv.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Create CV metadata without explicit JSON values
        cv_metadata = CVMetadataORM(
            file_id=file_metadata.id
        )
        test_db_session.add(cv_metadata)
        test_db_session.commit()
        test_db_session.refresh(cv_metadata)
        
        # Verify default JSON structures
        assert cv_metadata.primary_roles == []
        assert cv_metadata.industries_mentioned == []
        assert cv_metadata.skills_extracted == []
        assert cv_metadata.sections_extracted == {}

    def test_extraction_status_tracking(self, test_db_session: Session):
        """
        Test CV extraction status tracking and error handling.
        
        WHY: Enables proper tracking of async CV processing operations
        CONTRIBUTION: Provides visibility into processing status and error handling for operations team
        HOW: Tests extraction status flags and error message persistence
        """
        # Create base file
        file_metadata = FileMetadataORM(
            filename="processing_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv",
            minio_filename="processing-cv.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Create CV metadata with processing status
        cv_metadata = CVMetadataORM(
            file_id=file_metadata.id,
            extraction_completed=False,
            extraction_error="Text extraction failed: corrupted PDF"
        )
        test_db_session.add(cv_metadata)
        test_db_session.commit()
        test_db_session.refresh(cv_metadata)
        
        # Verify initial processing state
        assert cv_metadata.extraction_completed is False
        assert cv_metadata.extraction_error == "Text extraction failed: corrupted PDF"
        
        # Simulate successful processing
        cv_metadata.extraction_completed = True
        cv_metadata.extraction_error = None
        cv_metadata.skills_extracted = ["Python", "Machine Learning", "Data Analysis"]
        cv_metadata.primary_roles = ["Data Scientist", "Analyst"]
        
        test_db_session.commit()
        test_db_session.refresh(cv_metadata)
        
        # Verify successful processing state
        assert cv_metadata.extraction_completed is True
        assert cv_metadata.extraction_error is None
        assert "Python" in cv_metadata.skills_extracted
        assert "Data Scientist" in cv_metadata.primary_roles

    def test_current_cv_flag_management(self, test_db_session: Session):
        """
        Test current CV flag for user workflow management.
        
        WHY: Enables users to designate primary CV for cover letter generation
        CONTRIBUTION: Supports user workflow by identifying the most current CV version
        HOW: Tests current CV flag setting and ensures proper indexing for performance
        """
        # Create multiple CV files
        files = []
        cv_metadata_records = []
        
        for i in range(3):
            file_metadata = FileMetadataORM(
                filename=f"cv_version_{i}.pdf",
                file_type="cv",
                language="english",
                minio_bucket="cv",
                minio_filename=f"cv-version-{i}.pdf"
            )
            test_db_session.add(file_metadata)
            files.append(file_metadata)
        
        test_db_session.commit()
        
        for i, file_metadata in enumerate(files):
            test_db_session.refresh(file_metadata)
            cv_metadata = CVMetadataORM(
                file_id=file_metadata.id,
                is_current_cv=(i == 2)  # Only last one is current
            )
            test_db_session.add(cv_metadata)
            cv_metadata_records.append(cv_metadata)
        
        test_db_session.commit()
        
        # Query current CV
        current_cv = test_db_session.query(CVMetadataORM).filter(
            CVMetadataORM.is_current_cv == True
        ).first()
        
        assert current_cv is not None
        assert current_cv.file_metadata.filename == "cv_version_2.pdf"
        
        # Verify only one current CV exists
        current_cv_count = test_db_session.query(CVMetadataORM).filter(
            CVMetadataORM.is_current_cv == True
        ).count()
        
        assert current_cv_count == 1

    def test_sections_extracted_structure(self, test_db_session: Session):
        """
        Test sections_extracted JSON structure for future CV builder.
        
        WHY: Prepares data structure for future drag-drop CV builder functionality
        CONTRIBUTION: Enables structured CV section management and template generation
        HOW: Tests complex JSON structure storage and retrieval for CV sections
        """
        # Create base file
        file_metadata = FileMetadataORM(
            filename="structured_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv",
            minio_filename="structured-cv.pdf"
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Create CV metadata with complex sections structure
        sections_data = {
            "experience": [
                {
                    "company": "Tech Corp",
                    "title": "Data Scientist",
                    "duration": "2020-2023",
                    "description": "Led ML projects and data analysis"
                },
                {
                    "company": "Analytics Inc",
                    "title": "Junior Analyst", 
                    "duration": "2018-2020",
                    "description": "Performed data analysis and reporting"
                }
            ],
            "education": [
                {
                    "institution": "University ABC",
                    "degree": "MSc Data Science",
                    "year": "2018"
                }
            ],
            "skills": {
                "technical": ["Python", "SQL", "Machine Learning"],
                "soft": ["Communication", "Team Leadership"]
            }
        }
        
        cv_metadata = CVMetadataORM(
            file_id=file_metadata.id,
            sections_extracted=sections_data,
            extraction_completed=True
        )
        test_db_session.add(cv_metadata)
        test_db_session.commit()
        test_db_session.refresh(cv_metadata)
        
        # Verify complex JSON structure persistence
        assert "experience" in cv_metadata.sections_extracted
        assert "education" in cv_metadata.sections_extracted
        assert "skills" in cv_metadata.sections_extracted
        
        # Verify nested structure accessibility
        experience = cv_metadata.sections_extracted["experience"]
        assert len(experience) == 2
        assert experience[0]["company"] == "Tech Corp"
        assert experience[1]["title"] == "Junior Analyst"
        
        skills = cv_metadata.sections_extracted["skills"]
        assert "Python" in skills["technical"]
        assert "Communication" in skills["soft"]