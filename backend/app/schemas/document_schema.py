"""API response models for PDF textbook ingestion."""
from typing import Literal

from pydantic import BaseModel, Field


class DocumentIngestionResponse(BaseModel):
    source: str
    status: Literal["indexed", "skipped", "failed"]
    chunks_indexed: int = Field(ge=0)
    message: str


class DocumentUploadResponse(BaseModel):
    documents: list[DocumentIngestionResponse]


class DocumentStatusResponse(BaseModel):
    chunks: int = Field(ge=0)
    sources: int = Field(ge=0)
    pdf_files: int = Field(ge=0)
    indexed_files: int = Field(ge=0)


class UploadedDocumentResponse(BaseModel):
    filename: str
    source: str
    status: str
    chunks_indexed: int = Field(ge=0)


class UploadedDocumentListResponse(BaseModel):
    documents: list[UploadedDocumentResponse]


class DocumentDeletionResponse(BaseModel):
    source: str
    chunks_removed: int = Field(ge=0)
    message: str
