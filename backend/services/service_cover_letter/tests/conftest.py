# File: tests/conftest.py
"""
Test configuration and fixtures for file metadata management tests.

WHY: Provides isolated test database setup and fixtures for consistent testing environment
CONTRIBUTION: Ensures test reproducibility and proper test isolation for SonarCube coverage analysis
HOW: Creates temporary test database, mock connections, and reusable fixtures for file metadata testing
"""

import pytest
import tempfile
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

# Import our models and connection
from src.models.database.postgresql.file_metadata_models import (
    FileMetadataORM,
    TemplateMetadataORM,
    CVMetadataORM,
    JobtypeORM,
    IndustryORM
)
from src.config.config_db_connections import PostgressConnection


@pytest.fixture(scope="function")
def test_db_engine():
    """
    Create a test PostgreSQL database engine for testing.
    
    WHY: Provides isolated database environment that matches production PostgreSQL setup
    CONTRIBUTION: Enables accurate tests with PostgreSQL-specific features (JSONB, constraints, indexes)
    HOW: Uses test PostgreSQL database with proper cleanup between tests
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Create connection to test database (use a separate test database)
    # We'll use the same credentials but a different database name
    db_user = "cover_letter_user"
    db_pass = "cover_letter_pass"
    db_host = "localhost"
    db_port = "5432"
    
    # Use a test-specific database to avoid affecting production
    test_db_name = "cover_letter_test_db"
    
    # First, connect to postgres to create the test database if needed
    from sqlalchemy import text
    admin_engine = create_engine(
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/postgres",
        isolation_level="AUTOCOMMIT"
    )
    
    with admin_engine.connect() as conn:
        # Check if test database exists
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": test_db_name}
        )
        if not result.fetchone():
            # Create test database
            conn.execute(text(f"CREATE DATABASE {test_db_name}"))
    
    admin_engine.dispose()
    
    # Now connect to the test database
    engine = create_engine(
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{test_db_name}",
        echo=False  # Set to True for SQL debugging
    )
    
    # Create all tables
    PostgressConnection.Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup - drop all tables but keep the database for next run
    PostgressConnection.Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """
    Create database session for testing.
    
    WHY: Provides transaction-based test isolation with automatic rollback
    CONTRIBUTION: Ensures each test starts with clean database state for reliable test coverage
    HOW: Creates session with automatic transaction management and cleanup
    """
    SessionLocal = sessionmaker(bind=test_db_engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        # Close session and rollback any uncommitted changes
        session.close()


@pytest.fixture
def sample_jobtype(test_db_session) -> JobtypeORM:
    """
    Create sample jobtype for testing.
    
    WHY: Provides consistent test data for jobtype-related tests and foreign key relationships
    CONTRIBUTION: Supports test scenarios that require valid jobtype references
    HOW: Creates and persists jobtype record with standardized test attributes
    """
    jobtype = JobtypeORM(
        name="data_scientist",
        category="analytics", 
        is_active=True,
        description="Test data science role"
    )
    test_db_session.add(jobtype)
    test_db_session.commit()
    test_db_session.refresh(jobtype)
    return jobtype


@pytest.fixture
def sample_industry(test_db_session) -> IndustryORM:
    """
    Create sample industry for testing.
    
    WHY: Provides consistent test data for industry-related tests and categorization
    CONTRIBUTION: Supports test scenarios requiring valid industry references  
    HOW: Creates and persists industry record with standardized test attributes
    """
    industry = IndustryORM(
        name="technology",
        sector="tech",
        is_active=True,
        description="Test technology sector"
    )
    test_db_session.add(industry)
    test_db_session.commit()
    test_db_session.refresh(industry)
    return industry


@pytest.fixture
def sample_file_metadata(test_db_session) -> FileMetadataORM:
    """
    Create sample file metadata for testing.
    
    WHY: Provides base file metadata record for testing file operations and relationships
    CONTRIBUTION: Enables tests for file lifecycle management and metadata persistence
    HOW: Creates file metadata with realistic MinIO and content attributes for testing
    """
    file_metadata = FileMetadataORM(
        filename="test_template.pdf",
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
    return file_metadata


@pytest.fixture 
def sample_template_metadata(test_db_session, sample_file_metadata, sample_jobtype) -> TemplateMetadataORM:
    """
    Create sample template metadata for testing.
    
    WHY: Provides template-specific metadata for testing template categorization and business logic
    CONTRIBUTION: Enables testing of template recommendation engine and LLM context features
    HOW: Creates template metadata linked to base file with jobtype relationship for comprehensive testing
    """
    template_metadata = TemplateMetadataORM(
        file_id=sample_file_metadata.id,
        jobtype=sample_jobtype.name,
        industry_sectors=["technology", "finance"],
        template_subtype="cover_letter",
        company_size_target="any",
        effectiveness_score=0.8
    )
    test_db_session.add(template_metadata)
    test_db_session.commit()
    test_db_session.refresh(template_metadata)
    return template_metadata


@pytest.fixture
def sample_cv_metadata(test_db_session) -> CVMetadataORM:
    """
    Create sample CV metadata for testing.
    
    WHY: Provides CV-specific metadata for testing CV processing and experience tracking
    CONTRIBUTION: Enables testing of CV analysis features and role matching logic
    HOW: Creates CV metadata with realistic experience data and skill extraction results
    """
    # Create separate file metadata for CV
    cv_file_metadata = FileMetadataORM(
        filename="test_cv.pdf",
        file_type="cv", 
        language="english",
        minio_bucket="cv",
        minio_filename=f"{uuid.uuid4()}.pdf",
        original_content_type="application/pdf",
        file_size=204800
    )
    test_db_session.add(cv_file_metadata)
    test_db_session.commit()
    test_db_session.refresh(cv_file_metadata)
    
    cv_metadata = CVMetadataORM(
        file_id=cv_file_metadata.id,
        primary_roles=["Data Scientist", "ML Engineer"],
        experience_years=5,
        industries_mentioned=["technology", "healthcare"],
        skills_extracted=["Python", "Machine Learning", "SQL"],
        is_current_cv=True,
        sections_extracted={"experience": [], "education": [], "skills": []},
        extraction_completed=True
    )
    test_db_session.add(cv_metadata)
    test_db_session.commit()
    test_db_session.refresh(cv_metadata)
    return cv_metadata


@pytest.fixture
def multiple_jobtypes(test_db_session) -> list[JobtypeORM]:
    """
    Create multiple jobtypes for testing uniqueness and active state management.
    
    WHY: Provides test data for testing jobtype uniqueness constraints and lifecycle management
    CONTRIBUTION: Enables comprehensive testing of jobtype management features for complete coverage
    HOW: Creates multiple jobtype records with varied active states and categories
    """
    jobtypes = [
        JobtypeORM(name="data_scientist", category="analytics", is_active=True, description="Data science roles"),
        JobtypeORM(name="data_engineer", category="engineering", is_active=True, description="Data engineering roles"),
        JobtypeORM(name="deprecated_role", category="old", is_active=False, description="Deprecated job type"),
        JobtypeORM(name="analyst", category="analytics", is_active=True, description="Analysis roles")
    ]
    
    test_db_session.add_all(jobtypes)
    test_db_session.commit()
    
    for jobtype in jobtypes:
        test_db_session.refresh(jobtype)
        
    return jobtypes


@pytest.fixture
def mock_minio_file_data():
    """
    Mock MinIO file data for testing file operations.
    
    WHY: Provides realistic file data structure for testing without actual MinIO dependencies
    CONTRIBUTION: Enables testing of file processing logic with consistent mock data
    HOW: Returns dictionary with typical file upload attributes from FastAPI UploadFile
    """
    return {
        "filename": "cover_letter_template.pdf",
        "content_type": "application/pdf",
        "size": 102400,
        "content": b"Mock PDF content for testing"
    }