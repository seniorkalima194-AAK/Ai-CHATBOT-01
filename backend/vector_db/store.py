"""Persistent JSON vector store used by the local RAG pipeline.

The checked-in biology index lives at ``data/chroma/educational_materials.json``.
Keeping the reader and writer on that same file is essential: otherwise newly
indexed books are written to one store while questions are searched in another.
"""
from __future__ import annotations

import json
import os
from typing import Any, Sequence

from app.core.config import settings


COLLECTION_NAME = "educational_materials"
EXPECTED_DIM = 384
INDEX_FILE = settings.vector_db_path / f"{COLLECTION_NAME}.json"


def _load() -> dict[str, dict[str, Any]]:
    """Load the complete local index, returning an empty index when absent."""
    if not INDEX_FILE.exists():
        return {}

    with INDEX_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, dict):
        raise ValueError(f"Invalid vector index format: {INDEX_FILE}")
    return records


def load_records() -> list[dict[str, Any]]:
    """Return records for read-side cosine-similarity retrieval."""
    return list(_load().values())


def _validate_chunks(
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    sources: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    lengths = {
        "ids": len(ids),
        "embeddings": len(embeddings),
        "documents": len(documents),
        "sources": len(sources),
        "pages": len(pages),
        "chunk_indices": len(chunk_indices),
    }
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Mismatched batch lengths: {lengths}")

    for identifier, vector in zip(ids, embeddings):
        if len(vector) != EXPECTED_DIM:
            raise ValueError(
                f"Embedding {identifier} has {len(vector)} dimensions; "
                f"expected {EXPECTED_DIM}."
            )


def _upsert_into(
    records: dict[str, dict[str, Any]],
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    sources: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    """Apply validated chunks to an in-memory index."""
    for identifier, vector, document, source, page, chunk_index in zip(
        ids, embeddings, documents, sources, pages, chunk_indices
    ):
        records[identifier] = {
            "id": identifier,
            "embedding": list(vector),
            "document": str(document),
            "metadata": {
                "source": str(source),
                "page": int(page),
                "chunk_index": int(chunk_index),
            },
        }


def _write(records: dict[str, dict[str, Any]]) -> None:
    """Atomically replace the index so readers never see a partial update."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = INDEX_FILE.with_suffix(f".{os.getpid()}.tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False)
    os.replace(temporary_file, INDEX_FILE)


def upsert_chunks(
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    sources: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    """Insert or replace chunks without creating duplicates on re-indexing."""
    _validate_chunks(ids, embeddings, documents, sources, pages, chunk_indices)

    records = _load()
    _upsert_into(records, ids, embeddings, documents, sources, pages, chunk_indices)
    _write(records)


def replace_source_chunks(
    source: str,
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    """Replace one textbook's chunks as one atomic index update.

    This prevents duplicate answers when a teacher uploads a corrected version
    of a PDF with the same name.
    """
    sources = [source] * len(ids)
    _validate_chunks(ids, embeddings, documents, sources, pages, chunk_indices)

    records = {
        identifier: record
        for identifier, record in _load().items()
        if str((record.get("metadata") or {}).get("source")) != source
    }
    _upsert_into(records, ids, embeddings, documents, sources, pages, chunk_indices)
    _write(records)


def count() -> int:
    """Return the number of indexed chunks."""
    return len(_load())


def collection_count() -> int:
    """Compatibility name used by the index-building script."""
    return count()


def index_summary() -> dict[str, int]:
    """Return lightweight counts for the document-management API."""
    records = _load()
    sources = {
        str((record.get("metadata") or {}).get("source", "unknown"))
        for record in records.values()
    }
    return {"chunks": len(records), "sources": len(sources)}


def reset() -> None:
    """Delete the local JSON index. Intended only for a deliberate full rebuild."""
    if INDEX_FILE.exists():
        INDEX_FILE.unlink()
