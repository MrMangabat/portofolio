# backend/services/service_cover_letter/src/data_models/kafka_models/producers/file_upload_event.py
from pydantic import BaseModel, StringConstraints
from typing import Literal
from typing_extensions import Annotated


class FileUploadedEvent(BaseModel):
    """
    Event schema representing a file that has been uploaded and is ready for processing.

    Purpose:
        Defines the required metadata for a newly uploaded file to trigger downstream embedding.

    Capabilities:
        - Encapsulates the minimum viable metadata needed by downstream services.
        - Validates structure and field values to avoid malformed events.
        - Serializable to JSON for Kafka transport.

    Reasoning:
        This schema enforces strict typing to prevent silent contract drift between producer and consumer.
        It avoids loosely typed dicts or dynamic objects, and should be versioned if modified.

    Version:
        v1.0.0
    """

    file_id: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    user_id: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    bucket: Literal["uploaded-cv", "uploaded-cover-letters", "uploaded-documents"]
    filename: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    content_type: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=5)
    ]
    upload_method: Literal["web", "api", "agent"]
