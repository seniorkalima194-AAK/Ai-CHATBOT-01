"""
Shared data shapes for the embedding/indexing pipeline.

Chunk is what document-ingestion-pipeline is expected to produce.
VectorRecord is what's actually stored in the vector database.
Keeping both as Pydantic models means a malformed chunk fails with a
clear validation error at load time, not a confusing KeyError three
function calls later.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Chunk(BaseModel):
    """One chunk of source text, as produced by the ingestion pipeline."""

    text: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    page: int = Field(..., ge=0)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank or whitespace-only")
        return v


class VectorRecord(BaseModel):
    """One embedded chunk, ready to be upserted into the vector store."""

    id: str = Field(..., min_length=1)
    embedding: list[float]
    document: str
    metadata: dict   