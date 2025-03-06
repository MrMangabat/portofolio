# backend/core_configuration/database_connections.py
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from minio import Minio
# from qdrant_client import QdrantClient

class PostgresConnection:
    """Handles PostgreSQL config connection."""
    def __init__(self, config):
        self.engine = create_engine(config.RELATIONAL_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def create_tables(self):
        """Create database tables."""
        self.Base.metadata.create_all(bind=self.engine)

class MinioConnection:
    """Handles MinIO connection."""
    def __init__(self, config):
        try:
            endpoint = config.MINIO_ENDPOINT
            self.client = Minio(
                endpoint=endpoint,
                access_key=config.MINIO_ROOT_USER,
                secret_key=config.MINIO_ROOT_PASSWORD,
                secure=False  # Set to True if using HTTPS
            )
        except Exception as e:
            # Log the exception
            logging.error(f"Error initializing MinIO client: {e}")
            raise

# class QdrantConnection:
#     """Handles Qdrant connection."""
#     def __init__(self, config):
#         self.client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
