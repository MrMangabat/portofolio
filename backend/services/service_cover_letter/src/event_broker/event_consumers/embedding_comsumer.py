# backend/event_broker/event_handlers/embedding_consumer.py

"""
Kafka consumer for file_uploaded events.

Purpose:
    - Listens to file upload events from Kafka.
    - Downloads the file from MinIO using file_id and bucket.
    - Extracts text and embeds it into Qdrant.

Reasoning:
    - Full decoupling between file upload and embedding logic.
    - Enables asynchronous, fault-tolerant processing of uploaded files.
"""

import json
import logging
import time
from typing import Dict
from kafka import KafkaConsumer
import os
from io import BytesIO

from backend.services.service_cover_letter.src.config.config_db_connections import MiniOConnection, QdrantConnection
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository
from src.data_repositories.qdrant_repository.CRUD_qdrant import QdrantCoverLetterRepository
from src.service_layer.embbing_file_service import FileEmbeddingService
from src.data_models.kafka_models.producers.file_upload_event import FileUploadedEvent

# Kafka config
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka_broker")
KAFKA_PORT = int(os.getenv("KAFKA_PORT", 9092))
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_FILE_UPLOADED", "file_uploaded")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "embedding_consumer_group")

logging.basicConfig(level=logging.INFO)

def process_event(event: Dict[str, str]) -> None:
    """
    Process a single file_uploaded Kafka event.

    Args:
        event (Dict[str, str]): Dictionary with file_id, filename, bucket, and metadata
    """
    try:
        # Initialize repository and service layer
        minio_client = MiniOConnection.get_minio_connection()
        qdrant_client = QdrantConnection()
        minio_repo = MinioRepository(minio_client)
        qdrant_repo = QdrantCoverLetterRepository(qdrant_client)
        embedding_service = FileEmbeddingService(qdrant_repository=qdrant_repo)

        # Download file from MinIO
        file_content: bytes = minio_repo.get_file(
            file_name=event["filename"],
            bucket_type=event["bucket"]
        )

        file_stream: BytesIO = BytesIO(file_content)

        # Run embedding
        success = embedding_service.embed_file(
            file_stream=file_stream,
            filename=event["filename"],
            file_id=event["file_id"],
            metadata=event.get("metadata", {})
        )

        if success:
            logging.info(f"✅ Embedded file: {event['filename']}")
        else:
            logging.error(f"❌ Failed to embed: {event['filename']}")

    except Exception as e:
        logging.error(f"Error processing event: {e}")

def start_consumer() -> None:
    """
    Starts the Kafka consumer to listen for file_uploaded events.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=f"{KAFKA_BROKER}:{KAFKA_PORT}",
        group_id=KAFKA_CONSUMER_GROUP,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    logging.info(f"Listening to Kafka topic '{KAFKA_TOPIC}'...")

    for message in consumer:
        logging.info(f"Received event: {message.value}")
        process_event(message.value)

# if __name__ == "__main__":
#     while True:
#         try:
#             start_consumer()
#         except Exception as e:
#             logging.error(f"Kafka consumer crashed: {e}")
#             time.sleep(5)
