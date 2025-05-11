# backend/event_broker/event_producers/file_uploaded_producer.py
"""
Kafka producer for file upload events.

Purpose:
    - Sends a message to Kafka when a new file is uploaded to MinIO.

Capabilities:
    - Connects to Kafka broker using kafka-python
    - Publishes a JSON-encoded message to the 'file_uploaded' topic using a strict schema

Reasoning:
    - Decouples file upload from downstream processing (e.g., embedding)
    - Enforces schema-level correctness for safe event propagation
"""

import json
import logging
from typing import Optional
from kafka import KafkaProducer
import os

from src.data_models.kafka_models.producers.file_upload_event import FileUploadedEvent


class FileUploadedProducer:
    """
    A Kafka producer class for publishing 'file_uploaded' events.
    """
    logging.info("\nInside File_uploaded_producer.py\n")
    def __init__(self) -> None:
        """
        Initializes the Kafka producer connection using values from the environment.
        """
        broker = os.getenv("KAFKA_BROKER", "kafka_broker")
        port = os.getenv("KAFKA_PORT", "9092")
        self.topic = os.getenv("KAFKA_TOPIC_FILE_UPLOADED", "file_uploaded")

        try:
            self.producer: KafkaProducer = KafkaProducer(
                bootstrap_servers=f"{broker}:{port}",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=3
            )
            logging.info(f"✅ Kafka producer connected to {broker}:{port}")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Kafka producer: {e}")
            raise

    def publish_file_uploaded(self, event: FileUploadedEvent) -> bool:
        """
        Publishes the file_uploaded event to Kafka.

        Args:
            event (FileUploadedEvent): Validated Pydantic event model

        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        try:
                if not isinstance(event, FileUploadedEvent):
                    raise TypeError(f"Expected FileUploadedEvent, got {type(event)}")
                
                payload = event.model_dump()
                self.producer.send(self.topic, value=payload)
                self.producer.flush()
                logging.info(f"FILE: file_uploaded_producer.py | publish_file_uploaded |")
                logging.info(f"✅ Published file_uploaded event to topic '{self.topic}': {event.model_dump_json()}")
                return True

        except Exception as e:
            logging.info(f"FILE: file_uploaded_producer.py | publish_file_uploaded |")
            logging.error(f"❌ Failed to publish file_uploaded event: {e}")
            return False
