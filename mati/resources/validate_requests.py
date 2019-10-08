from dataclasses import dataclass

from mati.types import DocumentType, ValidationInputType, ValidationType


@dataclass
class Document:
    file_name: str
    stream: bytes
    input_type: ValidationInputType
    validation_type: ValidationType
    document_type: DocumentType = None
    page: str = None


@dataclass
class ValidateRequest:
    identity_id: str
    documents: list([Document])
    country: str
    group: int = 0
