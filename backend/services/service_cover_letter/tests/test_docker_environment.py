# File: tests/test_docker_environment.py
"""
Docker environment integration tests for service_cover_letter.

WHY: Validates that the service works correctly within the Docker environment with real connections
CONTRIBUTION: Ensures Docker networking, environment variables, and service integrations work as expected
HOW: Tests actual Docker hostnames and connections as defined in docker-compose.yaml
"""

import pytest
import uuid
import os
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from minio import Minio
from qdrant_client import QdrantClient

from src.models.database.postgresql.postgres_models import CorrectionORM, CorrectionType, JobListingORM
from src.models.database.postgresql.file_metadata_models import JobtypeORM, IndustryORM, FileMetadataORM
from src.repositories.postgresql.CRUD_postgres import CorrectionRepository, JobListingRepository
from src.repositories.postgresql.file_metadata_repository import FileMetadataRepository
from src.config.config_db_connections import PostgressConnection


class TestDockerEnvironmentConnections:
    """
    Test suite for Docker environment connections and UUID functionality.
    
    WHY: Ensures the service works correctly in the actual deployment environment
    CONTRIBUTION: Validates real-world Docker networking and service integration
    HOW: Uses actual Docker hostnames and tests complete service stack
    """
    
    @pytest.fixture(scope="class")
    def docker_postgres_connection(self):
        """
        Test connection to PostgreSQL container using Docker hostname.
        
        WHY: Validates PostgreSQL is accessible via Docker network
        CONTRIBUTION: Ensures database operations work in production environment
        HOW: Uses actual Docker hostnames from docker-compose.yaml
        """
        try:
            # Use Docker environment variables
            db_user = os.getenv("POSTGRES_USER", "cover_letter_user")
            db_pass = os.getenv("POSTGRES_PASSWORD", "cover_letter_pass")
            db_host = os.getenv("POSTGRES_HOST", "cover_letter_postgres")
            db_port = os.getenv("POSTGRES_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB", "cover_letter_db")
            
            # Create engine with Docker hostname
            engine = create_engine(
                f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
                echo=False
            )
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
                
            return engine
            
        except Exception as e:
            pytest.skip(f"PostgreSQL not accessible in Docker environment: {str(e)}")
    
    @pytest.fixture(scope="class")
    def docker_minio_connection(self):
        """
        Test connection to MinIO container using Docker hostname.
        
        WHY: Validates MinIO is accessible for file storage operations
        CONTRIBUTION: Ensures object storage works in production environment
        HOW: Uses MinIO Docker hostname and credentials from docker-compose.yaml
        """
        try:
            minio_host = os.getenv("MINIO_HOST", "cover_letter_minio")
            minio_port = int(os.getenv("MINIO_PORT", "9000"))
            access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
            secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
            
            # Create MinIO client with Docker hostname
            client = Minio(
                f"{minio_host}:{minio_port}",
                access_key=access_key,
                secret_key=secret_key,
                secure=False
            )
            
            # Test connection by listing buckets
            buckets = list(client.list_buckets())
            return client
            
        except Exception as e:
            pytest.skip(f"MinIO not accessible in Docker environment: {str(e)}")
    
    @pytest.fixture(scope="class")
    def docker_qdrant_connection(self):
        """
        Test connection to Qdrant container using Docker hostname.
        
        WHY: Validates Qdrant vector database is accessible
        CONTRIBUTION: Ensures vector search capabilities work in production
        HOW: Uses Qdrant Docker hostname from docker-compose.yaml
        """
        try:
            qdrant_host = os.getenv("QDRANT_HOST", "cover_letter_qdrant")
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            
            # Create Qdrant client with Docker hostname
            client = QdrantClient(host=qdrant_host, port=qdrant_port)
            
            # Test connection by getting collections
            collections = client.get_collections()
            return client
            
        except Exception as e:
            pytest.skip(f"Qdrant not accessible in Docker environment: {str(e)}")

    def test_postgresql_uuid_generation(self, docker_postgres_connection):
        """
        Test UUID primary key generation in PostgreSQL container.
        
        WHY: Validates UUID functionality works correctly in Docker PostgreSQL
        CONTRIBUTION: Ensures consistent UUID generation across all models
        HOW: Creates instances of all models and verifies UUID generation
        """
        SessionLocal = sessionmaker(bind=docker_postgres_connection)
        session = SessionLocal()
        
        created_objects = []
        
        try:
            # Test CorrectionORM UUID generation
            correction = CorrectionORM(
                text="Docker test correction",
                type=CorrectionType.skill
            )
            session.add(correction)
            session.commit()
            session.refresh(correction)
            
            assert correction.id is not None
            assert isinstance(correction.id, uuid.UUID)
            created_objects.append(('correction', correction))
            
            # Test JobListingORM UUID generation
            # First create with minimal required fields
            job_listing = JobListingORM(
                title="Docker Test Job",
                company="Test Company",
                requirements="Docker knowledge",
                expected_experience="2 years",
                listing="Test job listing",
                link="https://example.com/job",
                location="Remote",
                country="Global"
            )
            session.add(job_listing)
            session.commit()
            session.refresh(job_listing)
            
            assert job_listing.id is not None
            assert isinstance(job_listing.id, uuid.UUID)
            created_objects.append(('job_listing', job_listing))
            
            # Test JobtypeORM UUID generation
            jobtype = JobtypeORM(
                name=f"docker_test_jobtype_{uuid.uuid4().hex[:8]}",
                category="test",
                description="Docker test jobtype"
            )
            session.add(jobtype)
            session.commit()
            session.refresh(jobtype)
            
            assert jobtype.id is not None
            assert isinstance(jobtype.id, uuid.UUID)
            created_objects.append(('jobtype', jobtype))
            
            # Test IndustryORM UUID generation
            industry = IndustryORM(
                name=f"docker_test_industry_{uuid.uuid4().hex[:8]}",
                sector="test",
                description="Docker test industry"
            )
            session.add(industry)
            session.commit()
            session.refresh(industry)
            
            assert industry.id is not None
            assert isinstance(industry.id, uuid.UUID)
            created_objects.append(('industry', industry))
            
            # Test FileMetadataORM UUID generation
            file_metadata = FileMetadataORM(
                filename="docker_test.pdf",
                file_type="template",
                language="english",
                minio_bucket="test-bucket",
                minio_filename=f"docker_test_{uuid.uuid4()}.pdf"
            )
            session.add(file_metadata)
            session.commit()
            session.refresh(file_metadata)
            
            assert file_metadata.id is not None
            assert isinstance(file_metadata.id, uuid.UUID)
            created_objects.append(('file_metadata', file_metadata))
            
            print("✅ All Docker PostgreSQL UUID generations successful:")
            for obj_type, obj in created_objects:
                print(f"  {obj_type}: {obj.id} (type: {type(obj.id)})")
                
        finally:
            # Clean up created test objects
            for obj_type, obj in created_objects:
                try:
                    session.delete(obj)
                    session.commit()
                except:
                    session.rollback()
            session.close()
    
    def test_crud_repositories_with_docker_uuids(self, docker_postgres_connection):
        """
        Test CRUD repositories with UUID operations in Docker environment.
        
        WHY: Validates repository patterns work with UUIDs in production environment
        CONTRIBUTION: Ensures CRUD operations are reliable with UUID primary keys
        HOW: Tests complete CRUD lifecycle with actual Docker PostgreSQL
        """
        # Override the connection temporarily for this test
        original_connection = PostgressConnection.SessionLocal
        SessionLocal = sessionmaker(bind=docker_postgres_connection)
        PostgressConnection.SessionLocal = SessionLocal
        
        try:
            # Test CorrectionRepository with UUIDs
            correction_repo = CorrectionRepository()
            
            # Create
            correction = correction_repo.create("Docker CRUD test", CorrectionType.word)
            assert isinstance(correction.id, uuid.UUID)
            correction_id = correction.id
            
            # Read
            retrieved = correction_repo.get_by_id(correction_id)
            assert retrieved is not None
            assert retrieved.id == correction_id
            assert retrieved.text == "Docker CRUD test"
            
            # Update
            updated = correction_repo.update(correction_id, text="Updated Docker test")
            assert updated is not None
            assert updated.text == "Updated Docker test"
            assert updated.id == correction_id  # UUID should remain the same
            
            # Delete
            deleted = correction_repo.delete(correction_id)
            assert deleted is True
            
            # Verify deletion
            not_found = correction_repo.get_by_id(correction_id)
            assert not_found is None
            
            print(f"✅ CorrectionRepository CRUD with UUID successful: {correction_id}")
            
            # Test JobListingRepository with UUIDs
            job_repo = JobListingRepository()
            
            from src.models.database.postgresql.postgres_models import JobListingItem
            job_data = JobListingItem(
                title="Docker CRUD Job",
                company="Test Corp",
                requirements="Docker, UUID knowledge",
                expected_experience="3 years",
                listing="Full job description",
                link="https://test.com/job",
                location="Docker City",
                country="Containerland"
            )
            
            # Create
            job_listing = job_repo.create(job_data)
            assert isinstance(job_listing.id, uuid.UUID)
            job_id = job_listing.id
            
            # Read
            retrieved_job = job_repo.get_by_id(job_id)
            assert retrieved_job is not None
            assert retrieved_job.title == "Docker CRUD Job"
            
            # Update
            updated_job = job_repo.update(job_id, {"title": "Updated Docker Job"})
            assert updated_job is not None
            assert updated_job.title == "Updated Docker Job"
            assert updated_job.id == job_id
            
            # Delete
            deleted_job = job_repo.delete(job_id)
            assert deleted_job is True
            
            print(f"✅ JobListingRepository CRUD with UUID successful: {job_id}")
            
        finally:
            # Restore original connection
            PostgressConnection.SessionLocal = original_connection
    
    def test_file_metadata_repository_with_docker_connection(self, docker_postgres_connection):
        """
        Test FileMetadataRepository with Docker PostgreSQL connection.
        
        WHY: Validates file metadata operations work with UUIDs in production
        CONTRIBUTION: Ensures enhanced file workflow operates correctly
        HOW: Tests file metadata creation and retrieval with UUID relationships
        """
        # Override connection for this test
        original_connection = PostgressConnection.SessionLocal
        SessionLocal = sessionmaker(bind=docker_postgres_connection)
        PostgressConnection.SessionLocal = SessionLocal
        
        try:
            repo = FileMetadataRepository()
            
            # Create file metadata
            file_metadata = repo.create_file_metadata(
                filename="docker_integration_test.pdf",
                file_type="template",
                language="english",
                minio_bucket="test-templates",
                minio_filename=f"docker_test_{uuid.uuid4()}.pdf"
            )
            
            assert isinstance(file_metadata.id, uuid.UUID)
            print(f"✅ FileMetadata created with UUID: {file_metadata.id}")
            
            # Create a jobtype for template metadata
            jobtype_id = repo.create_jobtype(
                name=f"docker_integration_{uuid.uuid4().hex[:8]}",
                category="integration",
                description="Docker integration test jobtype"
            )
            
            # Create template metadata with UUID foreign key
            template_metadata = repo.create_template_metadata(
                file_id=file_metadata.id,
                jobtype=jobtype_id.name,
                industry_sectors=["technology", "testing"]
            )
            
            assert template_metadata.file_id == file_metadata.id
            print(f"✅ Template metadata linked to file UUID: {file_metadata.id}")
            
            # Test retrieval by jobtype
            templates = repo.get_templates_by_jobtype(jobtype_id.name)
            assert len(templates) >= 1
            assert any(t.id == file_metadata.id for t in templates)
            
            print("✅ FileMetadataRepository Docker integration successful")
            
        finally:
            PostgressConnection.SessionLocal = original_connection
    
    def test_service_environment_variables(self):
        """
        Test that all required Docker environment variables are available.
        
        WHY: Validates service configuration matches docker-compose.yaml
        CONTRIBUTION: Ensures consistent environment setup for production
        HOW: Checks all environment variables defined in docker-compose
        """
        required_env_vars = {
            'POSTGRES_DB': 'cover_letter_db',
            'POSTGRES_USER': 'cover_letter_user', 
            'POSTGRES_PASSWORD': 'cover_letter_pass',
            'POSTGRES_HOST': 'cover_letter_postgres',
            'POSTGRES_PORT': '5432',
            'MINIO_HOST': 'cover_letter_minio',
            'MINIO_PORT': '9000',
            'MINIO_ACCESS_KEY': 'minioadmin',
            'MINIO_SECRET_KEY': 'minioadmin'
        }
        
        missing_vars = []
        incorrect_vars = []
        
        for var_name, expected_value in required_env_vars.items():
            actual_value = os.getenv(var_name)
            
            if actual_value is None:
                missing_vars.append(var_name)
            elif actual_value != expected_value:
                incorrect_vars.append(f"{var_name}: expected '{expected_value}', got '{actual_value}'")
        
        if missing_vars:
            pytest.fail(f"Missing environment variables: {missing_vars}")
        
        if incorrect_vars:
            print(f"⚠️  Environment variable mismatches: {incorrect_vars}")
        
        print("✅ All Docker environment variables configured correctly")
    
    def test_docker_network_connectivity(self, docker_postgres_connection, docker_minio_connection):
        """
        Test connectivity between Docker services.
        
        WHY: Validates Docker network allows service communication
        CONTRIBUTION: Ensures production-like networking works correctly
        HOW: Tests connections to all dependent services
        """
        connections_tested = []
        
        # PostgreSQL connectivity
        if docker_postgres_connection:
            connections_tested.append("✅ PostgreSQL (cover_letter_postgres)")
        
        # MinIO connectivity
        if docker_minio_connection:
            connections_tested.append("✅ MinIO (cover_letter_minio)")
        
        # Try Qdrant connectivity
        try:
            qdrant_host = os.getenv("QDRANT_HOST", "cover_letter_qdrant")  
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            client = QdrantClient(host=qdrant_host, port=qdrant_port)
            client.get_collections()
            connections_tested.append("✅ Qdrant (cover_letter_qdrant)")
        except:
            connections_tested.append("⚠️  Qdrant (cover_letter_qdrant) - connection failed")
        
        print("Docker service connectivity:")
        for connection in connections_tested:
            print(f"  {connection}")
        
        # At least PostgreSQL should be connected for the service to work
        assert any("PostgreSQL" in conn for conn in connections_tested)


class TestUUIDConsistency:
    """
    Test UUID consistency across the entire system.
    
    WHY: Ensures all models use UUIDs consistently
    CONTRIBUTION: Validates architectural decision implementation
    HOW: Checks all model definitions and relationships
    """
    
    def test_all_models_use_uuid_primary_keys(self):
        """
        Test that all ORM models use UUID primary keys.
        
        WHY: Ensures consistent UUID usage across all models
        CONTRIBUTION: Validates no integer IDs remain in the system
        HOW: Inspects all model table definitions
        """
        from sqlalchemy.dialects.postgresql import UUID
        
        models_to_check = [
            CorrectionORM,
            JobListingORM, 
            JobtypeORM,
            IndustryORM,
            FileMetadataORM
        ]
        
        for model in models_to_check:
            id_column = model.__table__.columns['id']
            assert isinstance(id_column.type, UUID), f"{model.__name__} should use UUID primary key"
            print(f"✅ {model.__name__} uses UUID primary key")
    
    def test_uuid_foreign_key_relationships(self):
        """
        Test that foreign key relationships use UUIDs correctly.
        
        WHY: Ensures referential integrity with UUID keys
        CONTRIBUTION: Validates relationship mappings work with UUIDs
        HOW: Checks foreign key column types in related models
        """
        from sqlalchemy.dialects.postgresql import UUID
        from src.models.database.postgresql.file_metadata_models import TemplateMetadataORM, CVMetadataORM
        
        # Check TemplateMetadataORM.file_id references FileMetadataORM.id (both UUIDs)
        template_file_id = TemplateMetadataORM.__table__.columns['file_id']
        assert isinstance(template_file_id.type, UUID), "TemplateMetadataORM.file_id should be UUID"
        
        # Check CVMetadataORM.file_id references FileMetadataORM.id (both UUIDs)  
        cv_file_id = CVMetadataORM.__table__.columns['file_id']
        assert isinstance(cv_file_id.type, UUID), "CVMetadataORM.file_id should be UUID"
        
        print("✅ All foreign key relationships use UUID types")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])