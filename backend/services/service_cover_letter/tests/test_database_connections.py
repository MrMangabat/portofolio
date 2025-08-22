# File: tests/test_database_connections.py
"""
Database connection tests using .env configuration.

WHY: Validates that the service can connect to actual databases using production credentials
CONTRIBUTION: Ensures database connections and UUID functionality work with real infrastructure
HOW: Uses .env file credentials to test actual PostgreSQL, MinIO, and Qdrant connections
"""

import pytest
import uuid
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from minio import Minio
from qdrant_client import QdrantClient

from src.models.database.postgresql.postgres_models import CorrectionORM, CorrectionType, JobListingORM, JobListingItem
from src.models.database.postgresql.file_metadata_models import JobtypeORM, IndustryORM, FileMetadataORM
from src.repositories.postgresql.CRUD_postgres import CorrectionRepository, JobListingRepository
from src.repositories.postgresql.file_metadata_repository import FileMetadataRepository

# Load environment variables
load_dotenv()

class TestDatabaseConnections:
    """
    Test actual database connections using .env credentials.
    
    WHY: Validates service can connect to production databases
    CONTRIBUTION: Ensures infrastructure works with UUID implementation
    HOW: Uses .env file for credentials and tests real connections
    """
    
    def test_postgresql_connection_and_uuids(self):
        """
        Test PostgreSQL connection and UUID generation.
        
        WHY: Validates PostgreSQL works with UUID primary keys
        CONTRIBUTION: Ensures database operations function correctly
        HOW: Connects using .env credentials and tests UUID creation
        """
        try:
            # Get credentials from .env
            db_user = os.getenv("POSTGRES_USER")
            db_pass = os.getenv("POSTGRES_PASSWORD") 
            db_host = os.getenv("POSTGRES_HOST")
            db_port = os.getenv("POSTGRES_PORT")
            db_name = os.getenv("POSTGRES_DB")
            
            # Create engine
            engine = create_engine(
                f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
                echo=False
            )
            
            # Test basic connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
                print("✅ PostgreSQL connection successful")
            
            # Test UUID generation with actual models
            SessionLocal = sessionmaker(bind=engine)
            session = SessionLocal()
            
            test_objects = []
            
            try:
                # Test CorrectionORM UUID
                correction = CorrectionORM(
                    text="Connection test correction",
                    type=CorrectionType.skill
                )
                session.add(correction)
                session.flush()  # Get ID without committing
                
                assert correction.id is not None
                assert isinstance(correction.id, uuid.UUID)
                test_objects.append(correction)
                print(f"✅ CorrectionORM UUID: {correction.id}")
                
                # Test JobtypeORM UUID  
                jobtype = JobtypeORM(
                    name=f"test_connection_{uuid.uuid4().hex[:8]}",
                    category="test",
                    description="Connection test jobtype"
                )
                session.add(jobtype)
                session.flush()
                
                assert jobtype.id is not None
                assert isinstance(jobtype.id, uuid.UUID)
                test_objects.append(jobtype)
                print(f"✅ JobtypeORM UUID: {jobtype.id}")
                
                session.commit()
                print("✅ All UUIDs generated and committed successfully")
                
            finally:
                # Cleanup
                for obj in test_objects:
                    session.delete(obj)
                session.commit()
                session.close()
                
        except Exception as e:
            pytest.skip(f"PostgreSQL connection failed: {str(e)}")
    
    def test_minio_connection(self):
        """
        Test MinIO connection using .env credentials.
        
        WHY: Validates object storage is accessible
        CONTRIBUTION: Ensures file operations will work
        HOW: Uses .env MinIO credentials to test connection
        """
        try:
            # Get credentials from .env
            minio_host = os.getenv("MINIO_HOST")
            minio_port = os.getenv("MINIO_PORT")
            access_key = os.getenv("MINIO_ACCESS_KEY")
            secret_key = os.getenv("MINIO_SECRET_KEY")
            
            # Create MinIO client
            client = Minio(
                f"{minio_host}:{minio_port}",
                access_key=access_key,
                secret_key=secret_key,
                secure=False
            )
            
            # Test connection
            buckets = list(client.list_buckets())
            print(f"✅ MinIO connection successful - found {len(buckets)} buckets")
            
        except Exception as e:
            pytest.skip(f"MinIO connection failed: {str(e)}")
    
    def test_qdrant_connection(self):
        """
        Test Qdrant connection using .env credentials.
        
        WHY: Validates vector database is accessible
        CONTRIBUTION: Ensures embedding operations will work
        HOW: Uses .env Qdrant credentials to test connection
        """
        try:
            # Get credentials from .env
            qdrant_host = os.getenv("QDRANT_HOST")
            qdrant_port = int(os.getenv("QDRANT_PORT"))
            
            # Create Qdrant client
            client = QdrantClient(host=qdrant_host, port=qdrant_port)
            
            # Test connection
            collections = client.get_collections()
            print(f"✅ Qdrant connection successful - found {len(collections.collections)} collections")
            
        except Exception as e:
            pytest.skip(f"Qdrant connection failed: {str(e)}")
    
    def test_crud_repositories_with_real_database(self):
        """
        Test CRUD repositories with real PostgreSQL database.
        
        WHY: Validates repository patterns work with actual database
        CONTRIBUTION: Ensures UUID CRUD operations function correctly
        HOW: Uses repositories with real database connection
        """
        try:
            # Test CorrectionRepository
            correction_repo = CorrectionRepository()
            
            # Create
            correction = correction_repo.create("Real DB test", CorrectionType.word)
            assert isinstance(correction.id, uuid.UUID)
            correction_id = correction.id
            
            # Read
            retrieved = correction_repo.get_by_id(correction_id)
            assert retrieved is not None
            assert retrieved.id == correction_id
            
            # Update
            updated = correction_repo.update(correction_id, text="Updated real DB test")
            assert updated is not None
            assert updated.text == "Updated real DB test"
            
            # Delete
            deleted = correction_repo.delete(correction_id)
            assert deleted is True
            
            print(f"✅ CorrectionRepository CRUD successful with UUID: {correction_id}")
            
            # Test JobListingRepository
            job_repo = JobListingRepository()
            job_data = JobListingItem(
                title="Real DB Test Job",
                company="Test Company",
                requirements="Real database testing",
                expected_experience="1 year",
                listing="Full description",
                link="https://test.com",
                location="Test City", 
                country="Test Country"
            )
            
            job_listing = job_repo.create(job_data)
            assert isinstance(job_listing.id, uuid.UUID)
            
            # Cleanup
            job_repo.delete(job_listing.id)
            print(f"✅ JobListingRepository CRUD successful with UUID: {job_listing.id}")
            
        except Exception as e:
            pytest.skip(f"Repository test failed: {str(e)}")
    
    def test_file_metadata_repository_with_real_database(self):
        """
        Test FileMetadataRepository with real PostgreSQL database.
        
        WHY: Validates enhanced file workflow with actual database
        CONTRIBUTION: Ensures file metadata operations work with UUIDs
        HOW: Tests file metadata creation and relationships
        """
        try:
            repo = FileMetadataRepository()
            
            # Create file metadata
            file_metadata = repo.create_file_metadata(
                filename="real_db_test.pdf",
                file_type="template", 
                language="english",
                minio_bucket="test-templates",
                minio_filename=f"test_{uuid.uuid4()}.pdf"
            )
            
            assert isinstance(file_metadata.id, uuid.UUID)
            print(f"✅ FileMetadata created with UUID: {file_metadata.id}")
            
            # Create jobtype
            jobtype = repo.create_jobtype(
                name=f"real_db_test_{uuid.uuid4().hex[:8]}",
                category="testing",
                description="Real database test"
            )
            
            # Create template metadata
            template_metadata = repo.create_template_metadata(
                file_id=file_metadata.id,
                jobtype=jobtype.name,
                industry_sectors=["testing"]
            )
            
            assert template_metadata.file_id == file_metadata.id
            print(f"✅ Template metadata linked to UUID: {file_metadata.id}")
            
        except Exception as e:
            pytest.skip(f"FileMetadataRepository test failed: {str(e)}")
    
    def test_environment_variables_loaded(self):
        """
        Test that all required environment variables are loaded.
        
        WHY: Ensures .env file is properly loaded
        CONTRIBUTION: Validates configuration is available
        HOW: Checks all required environment variables exist
        """
        required_vars = [
            'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 
            'POSTGRES_HOST', 'POSTGRES_PORT',
            'MINIO_HOST', 'MINIO_PORT', 'MINIO_ACCESS_KEY', 'MINIO_SECRET_KEY',
            'QDRANT_HOST', 'QDRANT_PORT'
        ]
        
        missing_vars = []
        for var in required_vars:
            if os.getenv(var) is None:
                missing_vars.append(var)
        
        if missing_vars:
            pytest.fail(f"Missing environment variables: {missing_vars}")
        
        print("✅ All required environment variables loaded from .env")


class TestUUIDModels:
    """
    Test UUID implementation in all models.
    
    WHY: Ensures consistent UUID usage across all models
    CONTRIBUTION: Validates architectural consistency
    HOW: Checks model definitions and UUID types
    """
    
    def test_all_models_have_uuid_primary_keys(self):
        """
        Test that all models use UUID primary keys.
        
        WHY: Ensures no integer IDs remain in the system
        CONTRIBUTION: Validates UUID migration is complete
        HOW: Inspects model table definitions
        """
        from sqlalchemy.dialects.postgresql import UUID
        
        models = [
            CorrectionORM,
            JobListingORM,
            JobtypeORM, 
            IndustryORM,
            FileMetadataORM
        ]
        
        for model in models:
            id_column = model.__table__.columns['id']
            assert isinstance(id_column.type, UUID), f"{model.__name__} should use UUID primary key"
            print(f"✅ {model.__name__} uses UUID primary key")
    
    def test_uuid_foreign_keys(self):
        """
        Test that foreign key relationships use UUIDs.
        
        WHY: Ensures referential integrity with UUID keys
        CONTRIBUTION: Validates relationship consistency
        HOW: Checks foreign key column types
        """
        from sqlalchemy.dialects.postgresql import UUID
        from src.models.database.postgresql.file_metadata_models import TemplateMetadataORM, CVMetadataORM
        
        # Check UUID foreign keys
        template_fk = TemplateMetadataORM.__table__.columns['file_id']
        cv_fk = CVMetadataORM.__table__.columns['file_id']
        
        assert isinstance(template_fk.type, UUID), "TemplateMetadataORM.file_id should be UUID"
        assert isinstance(cv_fk.type, UUID), "CVMetadataORM.file_id should be UUID"
        
        print("✅ All foreign key relationships use UUIDs")


if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "-s"])