# backend/services/service_cover_letter/src/config/connections/postgres_connection.py
"""
PostgreSQL connection handler for the cover_letter service.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config.settings import CoverLetterSettings

settings_from_env = CoverLetterSettings()


class PostgresConnection:
    Base = declarative_base()
    engine = None
    SessionLocal = None

    @classmethod
    def initialize(cls) -> None:
        """
        Lazy initializer for engine and SessionLocal.
        Only called explicitly in FastAPI startup or actual usage contexts.
        """
        if cls.engine is None:
            try:
                cls.engine = create_engine(settings_from_env.POSTGRES_URL)
                cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Postgres connection: {e}")

    @staticmethod
    def get_db():
        if PostgresConnection.SessionLocal is None:
            raise RuntimeError("PostgresConnection was never initialized. Call initialize() first.")
        db = PostgresConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()
