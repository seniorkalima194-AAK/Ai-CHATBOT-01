"""Small persistent local vector store for the offline school chatbot.

The original Chroma integration crashes on this Windows/Python runtime. This
module keeps the same indexing contract using a transparent JSON file and lets
the retriever perform cosine search in pure Python. It is appropriate for the
current single-school PDF collection and can be replaced later if the corpus
grows substantially.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Sequence

from app.core.config import settings

COLLECTION_NAME = "educational_materials"
EXPECTED_DIM = 384
INDEX_FILE = settings.vector_db_path / f"{COLLECTION_NAME}.json"


def _load() -> dict[str, dict[str, Any]]:
    if not INDEX_FILE.exists():
        return {}
    with INDEX_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid vector index format: {INDEX_FILE}")
    return data


def load_records() -> list[dict[str, Any]]:
    """Return stored records for read-side retrieval."""
    return list(_load().values())


def upsert_chunks(
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    sources: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    lengths = [len(ids), len(embeddings), len(documents), len(sources), len(pages), len(chunk_indices)]
    if len(set(lengths)) != 1:
        raise ValueError(f"Mismatched batch lengths: {lengths}")

    records = _load()
    for identifier, vector, document, source, page, chunk_index in zip(
        ids, embeddings, documents, sources, pages, chunk_indices
    ):
        if len(vector) != EXPECTED_DIM:
            raise ValueError(
                f"Embedding {identifier} has {len(vector)} dimensions; expected {EXPECTED_DIM}."
            )
        records[identifier] = {
            "id": identifier,
            "embedding": list(vector),
            "document": document,
            "metadata": {
                "source": source,
                "page": page,
                "chunk_index": chunk_index,
            },
        }

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = INDEX_FILE.with_suffix(f".{os.getpid()}.tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False)
    os.replace(temporary_file, INDEX_FILE)


def count() -> int:
    return len(_load())


def collection_count() -> int:
    return count()


def upsert_records(records: Sequence[Any]) -> None:
    upsert_chunks(
        ids=[record.id for record in records],
        embeddings=[record.embedding for record in records],
        documents=[record.document for record in records],
        sources=[record.metadata["source"] for record in records],
        pages=[record.metadata["page"] for record in records],
        chunk_indices=[record.metadata.get("chunk_index", 0) for record in records],
    )


def reset() -> None:
    if INDEX_FILE.exists():
        INDEX_FILE.unlink()
