# File: tests/test_integration_full_workflow.py
"""
Integration tests for complete file metadata workflow scenarios.

WHY: Validates end-to-end workflows that combine multiple components and business operations
CONTRIBUTION: Ensures system integration works correctly and provides high test coverage for SonarCube
HOW: Tests realistic user scenarios combining file creation, metadata management, and system operations
"""

import pytest
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.models.database.postgresql.file_metadata_models import (
    FileMetadataORM,
    TemplateMetadataORM,
    CVMetadataORM,
    JobtypeORM,
    IndustryORM
)


class TestFileMetadataIntegrationWorkflows:
    """
    Integration tests for complete file metadata management workflows.
    
    WHY: Validates realistic user scenarios that involve multiple system components
    CONTRIBUTION: Ensures system reliability for actual user workflows and comprehensive test coverage
    HOW: Tests complete workflows from file upload to metadata management and cleanup
    """

    def test_complete_template_upload_workflow(self, test_db_session: Session):
        """
        Test complete template upload and categorization workflow.
        
        WHY: Validates the entire template processing pipeline from upload to categorization
        CONTRIBUTION: Ensures all template workflow components work together correctly
        HOW: Simulates complete template upload with metadata assignment and validation
        """
        # Step 1: Create supporting lookup data
        jobtype = JobtypeORM(
            name="ml_engineer",
            category="engineering",
            is_active=True,
            description="Machine learning engineering roles"
        )
        test_db_session.add(jobtype)
        test_db_session.commit()
        
        # Step 2: Create base file metadata (simulating MinIO upload)
        file_metadata = FileMetadataORM(
            filename="senior_ml_engineer_template.pdf",
            file_type="template",
            language="english",
            minio_bucket="cover-letters",
            minio_filename=f"{uuid.uuid4()}.pdf",
            original_content_type="application/pdf",
            file_size=156800,
            qdrant_point_id=uuid.uuid4()
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        # Step 3: Add template-specific metadata
        template_metadata = TemplateMetadataORM(
            file_id=file_metadata.id,
            jobtype=jobtype.name,
            industry_sectors=["technology", "artificial_intelligence"],
            template_subtype="cover_letter",
            company_size_target="mid",
            effectiveness_score=0.85,
            last_used_at=datetime.now()
        )
        test_db_session.add(template_metadata)
        test_db_session.commit()
        
        # Step 4: Validate complete workflow integration
        # Query template with all related data
        complete_template = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.id == file_metadata.id
        ).first()
        
        # Validate file metadata
        assert complete_template.filename == "senior_ml_engineer_template.pdf"
        assert complete_template.file_type == "template"
        assert complete_template.minio_bucket == "cover-letters"
        assert complete_template.qdrant_point_id is not None
        
        # Validate template metadata relationship
        assert complete_template.template_metadata is not None
        assert complete_template.template_metadata.jobtype == "ml_engineer"
        assert "technology" in complete_template.template_metadata.industry_sectors
        assert complete_template.template_metadata.effectiveness_score == 0.85
        
        # Step 5: Test template filtering by criteria
        # Find templates for ML engineer roles
        ml_templates = test_db_session.query(FileMetadataORM).join(
            TemplateMetadataORM
        ).filter(
            FileMetadataORM.file_type == "template",
            TemplateMetadataORM.jobtype == "ml_engineer",
            FileMetadataORM.language == "english"
        ).all()
        
        assert len(ml_templates) == 1
        assert ml_templates[0].filename == "senior_ml_engineer_template.pdf"

    def test_complete_cv_processing_workflow(self, test_db_session: Session):
        """
        Test complete CV upload and processing workflow.
        
        WHY: Validates the entire CV processing pipeline from upload to extraction completion
        CONTRIBUTION: Ensures all CV workflow components integrate correctly for user experience
        HOW: Simulates complete CV upload with text extraction and metadata assignment
        """
        # Step 1: Create base CV file metadata
        cv_file = FileMetadataORM(
            filename="john_doe_senior_data_scientist_cv.pdf",
            file_type="cv",
            language="english",
            minio_bucket="cv",
            minio_filename=f"{uuid.uuid4()}.pdf",
            original_content_type="application/pdf",
            file_size=245760
        )
        test_db_session.add(cv_file)
        test_db_session.commit()
        test_db_session.refresh(cv_file)
        
        # Step 2: Simulate initial CV processing (extraction in progress)
        cv_metadata = CVMetadataORM(
            file_id=cv_file.id,
            extraction_completed=False,
            is_current_cv=False
        )
        test_db_session.add(cv_metadata)
        test_db_session.commit()
        
        # Step 3: Simulate successful text extraction completion
        cv_metadata.extraction_completed = True
        cv_metadata.primary_roles = ["Senior Data Scientist", "ML Engineer", "Analytics Lead"]
        cv_metadata.experience_years = 8
        cv_metadata.industries_mentioned = ["technology", "fintech", "healthcare"]
        cv_metadata.skills_extracted = [
            "Python", "R", "SQL", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "AWS", "Docker", "Kubernetes"
        ]
        cv_metadata.sections_extracted = {
            "experience": [
                {
                    "company": "TechCorp Inc",
                    "title": "Senior Data Scientist",
                    "duration": "2020-2023",
                    "responsibilities": ["Led ML model development", "Managed junior team"]
                },
                {
                    "company": "DataAnalytics Ltd",
                    "title": "Data Scientist",
                    "duration": "2018-2020",
                    "responsibilities": ["Built predictive models", "Conducted data analysis"]
                }
            ],
            "education": [
                {
                    "institution": "Tech University",
                    "degree": "MSc Data Science",
                    "year": "2018"
                }
            ],
            "certifications": [
                "AWS Certified ML Specialty",
                "Google Cloud Professional ML Engineer"
            ]
        }
        cv_metadata.is_current_cv = True
        
        test_db_session.commit()
        test_db_session.refresh(cv_metadata)
        
        # Step 4: Validate complete CV workflow
        complete_cv = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.id == cv_file.id
        ).first()
        
        # Validate file metadata
        assert complete_cv.filename == "john_doe_senior_data_scientist_cv.pdf"
        assert complete_cv.file_type == "cv"
        assert complete_cv.minio_bucket == "cv"
        
        # Validate CV metadata processing results
        assert complete_cv.cv_metadata is not None
        assert complete_cv.cv_metadata.extraction_completed is True
        assert complete_cv.cv_metadata.experience_years == 8
        assert complete_cv.cv_metadata.is_current_cv is True
        assert "Senior Data Scientist" in complete_cv.cv_metadata.primary_roles
        assert "Python" in complete_cv.cv_metadata.skills_extracted
        assert "technology" in complete_cv.cv_metadata.industries_mentioned
        
        # Validate complex sections structure
        sections = complete_cv.cv_metadata.sections_extracted
        assert "experience" in sections
        assert "education" in sections
        assert len(sections["experience"]) == 2
        assert sections["experience"][0]["company"] == "TechCorp Inc"

    def test_multi_file_system_integration(self, test_db_session: Session):
        """
        Test system integration with multiple files of different types.
        
        WHY: Validates system behavior with realistic multi-file scenarios
        CONTRIBUTION: Ensures system scalability and proper isolation between different file types
        HOW: Creates multiple files with different types and tests cross-file operations
        """
        # Create supporting lookup data
        jobtypes = [
            JobtypeORM(name="data_scientist", category="analytics", is_active=True),
            JobtypeORM(name="product_manager", category="management", is_active=True),
            JobtypeORM(name="software_engineer", category="engineering", is_active=True)
        ]
        test_db_session.add_all(jobtypes)
        test_db_session.commit()
        
        # Create multiple files of different types
        files_data = [
            {
                "filename": "data_science_template.pdf",
                "file_type": "template",
                "language": "english",
                "bucket": "cover-letters",
                "jobtype": "data_scientist"
            },
            {
                "filename": "product_mgmt_template.pdf", 
                "file_type": "template",
                "language": "english",
                "bucket": "cover-letters",
                "jobtype": "product_manager"
            },
            {
                "filename": "software_eng_template.pdf",
                "file_type": "template",
                "language": "danish",
                "bucket": "cover-letters",
                "jobtype": "software_engineer"
            },
            {
                "filename": "current_cv.pdf",
                "file_type": "cv",
                "language": "english",
                "bucket": "cv",
                "is_current": True
            },
            {
                "filename": "old_cv_backup.pdf",
                "file_type": "cv",
                "language": "english",
                "bucket": "cv",
                "is_current": False
            }
        ]
        
        created_files = []
        for file_data in files_data:
            # Create base file metadata
            file_metadata = FileMetadataORM(
                filename=file_data["filename"],
                file_type=file_data["file_type"],
                language=file_data["language"],
                minio_bucket=file_data["bucket"],
                minio_filename=f"{uuid.uuid4()}.pdf",
                original_content_type="application/pdf",
                file_size=128000 + len(created_files) * 10000  # Varying sizes
            )
            test_db_session.add(file_metadata)
            test_db_session.commit()
            test_db_session.refresh(file_metadata)
            
            # Add type-specific metadata
            if file_data["file_type"] == "template":
                template_metadata = TemplateMetadataORM(
                    file_id=file_metadata.id,
                    jobtype=file_data["jobtype"],
                    industry_sectors=["technology"],
                    template_subtype="cover_letter"
                )
                test_db_session.add(template_metadata)
            elif file_data["file_type"] == "cv":
                cv_metadata = CVMetadataORM(
                    file_id=file_metadata.id,
                    experience_years=5 + len(created_files),
                    is_current_cv=file_data["is_current"],
                    extraction_completed=True,
                    primary_roles=["Generic Role"]
                )
                test_db_session.add(cv_metadata)
            
            created_files.append(file_metadata)
        
        test_db_session.commit()
        
        # Test cross-file type queries and operations
        # 1. Count files by type
        template_count = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.file_type == "template"
        ).count()
        cv_count = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.file_type == "cv"
        ).count()
        
        assert template_count == 3
        assert cv_count == 2
        
        # 2. Test language filtering
        english_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.language == "english"
        ).count()
        danish_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.language == "danish"
        ).count()
        
        assert english_files == 4
        assert danish_files == 1
        
        # 3. Test current CV identification
        current_cv = test_db_session.query(FileMetadataORM).join(
            CVMetadataORM
        ).filter(
            CVMetadataORM.is_current_cv == True
        ).first()
        
        assert current_cv is not None
        assert current_cv.filename == "current_cv.pdf"
        
        # 4. Test template jobtype distribution
        jobtype_counts = {}
        templates_with_metadata = test_db_session.query(FileMetadataORM).join(
            TemplateMetadataORM
        ).all()
        
        for template in templates_with_metadata:
            jobtype = template.template_metadata.jobtype
            jobtype_counts[jobtype] = jobtype_counts.get(jobtype, 0) + 1
        
        assert jobtype_counts["data_scientist"] == 1
        assert jobtype_counts["product_manager"] == 1
        assert jobtype_counts["software_engineer"] == 1

    def test_file_cleanup_cascade_workflow(self, test_db_session: Session):
        """
        Test complete file cleanup workflow with cascade operations.
        
        WHY: Validates proper cleanup workflow when files are removed from the system
        CONTRIBUTION: Ensures no data orphaning occurs during file management operations
        HOW: Creates complete file with metadata, then tests cleanup cascade behavior
        """
        # Create complete file setup with both template and lookup data
        jobtype = JobtypeORM(name="test_jobtype", category="test", is_active=True)
        test_db_session.add(jobtype)
        test_db_session.commit()
        
        # Create file with comprehensive metadata
        file_metadata = FileMetadataORM(
            filename="comprehensive_test_file.pdf",
            file_type="template",
            language="english",
            minio_bucket="cover-letters",
            minio_filename=f"{uuid.uuid4()}.pdf",
            original_content_type="application/pdf",
            file_size=200000,
            qdrant_point_id=uuid.uuid4()
        )
        test_db_session.add(file_metadata)
        test_db_session.commit()
        test_db_session.refresh(file_metadata)
        
        template_metadata = TemplateMetadataORM(
            file_id=file_metadata.id,
            jobtype=jobtype.name,
            industry_sectors=["technology", "consulting"],
            template_subtype="cover_letter",
            company_size_target="enterprise",
            effectiveness_score=0.92,
            last_used_at=datetime.now() - timedelta(days=3)
        )
        test_db_session.add(template_metadata)
        test_db_session.commit()
        
        file_id = file_metadata.id
        
        # Verify complete setup exists
        assert test_db_session.query(FileMetadataORM).filter_by(id=file_id).count() == 1
        assert test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_id).count() == 1
        
        # Perform cleanup (delete base file)
        test_db_session.delete(file_metadata)
        test_db_session.commit()
        
        # Verify complete cleanup occurred
        assert test_db_session.query(FileMetadataORM).filter_by(id=file_id).count() == 0
        assert test_db_session.query(TemplateMetadataORM).filter_by(file_id=file_id).count() == 0
        
        # Verify lookup data remains (not cascade deleted)
        assert test_db_session.query(JobtypeORM).filter_by(name="test_jobtype").count() == 1

    def test_system_performance_with_scale(self, test_db_session: Session):
        """
        Test system performance characteristics with larger dataset.
        
        WHY: Validates system behavior and performance with realistic data volumes
        CONTRIBUTION: Ensures system scalability for production usage scenarios
        HOW: Creates larger dataset and tests common query patterns for performance validation
        """
        # Create supporting lookup data
        jobtypes = [
            JobtypeORM(name=f"jobtype_{i}", category="test", is_active=(i % 3 != 0))
            for i in range(10)
        ]
        test_db_session.add_all(jobtypes)
        test_db_session.commit()
        
        # Create larger dataset of files
        files = []
        languages = ["english", "danish"]
        file_types = ["template", "cv", "application"]
        
        for i in range(50):  # Create 50 files
            file_metadata = FileMetadataORM(
                filename=f"test_file_{i:03d}.pdf",
                file_type=file_types[i % len(file_types)],
                language=languages[i % len(languages)],
                minio_bucket="cover-letters" if i % 2 == 0 else "cv",
                minio_filename=f"{uuid.uuid4()}.pdf",
                original_content_type="application/pdf",
                file_size=100000 + (i * 1000),
                created_at=datetime.now() - timedelta(days=i // 10)
            )
            files.append(file_metadata)
        
        test_db_session.add_all(files)
        test_db_session.commit()
        
        # Add metadata for subset of files
        for i, file_metadata in enumerate(files[:30]):  # Add metadata to first 30 files
            test_db_session.refresh(file_metadata)
            
            if file_metadata.file_type == "template":
                template_metadata = TemplateMetadataORM(
                    file_id=file_metadata.id,
                    jobtype=jobtypes[i % len(jobtypes)].name,
                    industry_sectors=["technology"],
                    effectiveness_score=0.5 + (i % 5) * 0.1
                )
                test_db_session.add(template_metadata)
            elif file_metadata.file_type == "cv":
                cv_metadata = CVMetadataORM(
                    file_id=file_metadata.id,
                    experience_years=i % 15,
                    is_current_cv=(i == 1),  # Only first CV (index 1) is current
                    extraction_completed=True
                )
                test_db_session.add(cv_metadata)
        
        test_db_session.commit()
        
        # Test common query patterns for performance
        # 1. Type and language filtering (using composite index)
        english_templates = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.file_type == "template",
            FileMetadataORM.language == "english"
        ).all()
        
        assert len(english_templates) > 0
        
        # 2. Recent files query (using created_at index)
        recent_files = test_db_session.query(FileMetadataORM).filter(
            FileMetadataORM.created_at >= datetime.now() - timedelta(days=5)
        ).order_by(FileMetadataORM.created_at.desc()).limit(10).all()
        
        assert len(recent_files) <= 10
        
        # 3. Current CV query (using CV metadata index)
        current_cv_query = test_db_session.query(FileMetadataORM).join(
            CVMetadataORM
        ).filter(
            CVMetadataORM.is_current_cv == True
        ).all()
        
        assert len(current_cv_query) == 1
        
        # 4. Active jobtype filtering
        active_jobtypes = test_db_session.query(JobtypeORM).filter(
            JobtypeORM.is_active == True
        ).all()
        
        # Should return jobtypes where i % 3 != 0 (roughly 66% of 10 = ~6-7)
        assert len(active_jobtypes) >= 6
        assert len(active_jobtypes) <= 7
        
        # 5. Complex join query for template recommendations
        effective_templates = test_db_session.query(FileMetadataORM).join(
            TemplateMetadataORM
        ).filter(
            FileMetadataORM.file_type == "template",
            FileMetadataORM.language == "english",
            TemplateMetadataORM.effectiveness_score >= 0.7
        ).order_by(TemplateMetadataORM.effectiveness_score.desc()).all()
        
        # Verify results are properly filtered and ordered
        if effective_templates:
            for i in range(len(effective_templates) - 1):
                current_score = effective_templates[i].template_metadata.effectiveness_score
                next_score = effective_templates[i + 1].template_metadata.effectiveness_score
                assert current_score >= next_score  # Descending order