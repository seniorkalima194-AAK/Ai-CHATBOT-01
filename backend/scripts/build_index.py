# Placeholder: script to build the vector index from processed documents.
"""
Reads chunked documents from data/processed/, embeds them, and upserts
them into the vector store via vector_db/store.py.

Expected input format (contract with document-ingestion-pipeline —
confirm it matches their actual output before running):
Each file in data/processed/ is a .jsonl file, one JSON object per line:
    {"text": "...", "source": "biology_ch3.pdf", "page": 12}

Idempotent by design: each chunk's id is a stable hash of
(source, page, text). Re-running this script on unchanged chunks
overwrites the same ids instead of creating duplicates. Run it with:
    cd backend && python -m scripts.build_index
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pydantic import ValidationError

from app.core.config import settings
from app.core.logging import logger
from app.rag.embeddings import embed_batch, validate_dimension
from app.schemas.vector_schema import Chunk
from vector_db.store import collection_count, upsert_chunks

PROCESSED_DIR = settings.processed_documents_path
UPSERT_BATCH_SIZE = 64


def _chunk_id(chunk: Chunk, chunk_index: int = 0) -> str:
    """Stable id from content — same chunk always maps to the same id."""
    digest = hashlib.sha256(
        f"{chunk.source}|{chunk.page}|{chunk_index}|{chunk.text}".encode("utf-8")
    ).hexdigest()
    return f"{chunk.source}::{chunk.page}::{digest[:16]}"


def _load_chunks(processed_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    files = sorted(processed_dir.glob("*.jsonl"))

    if not files:
        logger.warning("no_processed_files_found", path=str(processed_dir))
        return chunks

    for file_path in files:
        with file_path.open("r", encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    logger.warning(
                        "skipping_malformed_line",
                        file=file_path.name,
                        line=line_number,
                        error=str(exc),
                    )
                    continue

                try:
                    chunks.append(Chunk(**record))
                except ValidationError as exc:
                    logger.warning(
                        "skipping_invalid_chunk",
                        file=file_path.name,
                        line=line_number,
                        error=str(exc.errors()),
                    )
                    continue

    return chunks


def build_index() -> None:
    validate_dimension()

    chunks = _load_chunks(PROCESSED_DIR)
    if not chunks:
        logger.warning("build_index_no_chunks_to_process")
        return

    total = len(chunks)
    logger.info("build_index_started", total_chunks=total)

    for start in range(0, total, UPSERT_BATCH_SIZE):
        batch = chunks[start : start + UPSERT_BATCH_SIZE]
        vectors = embed_batch([c.text for c in batch])
        chunk_indices = list(range(start, start + len(batch)))
        upsert_chunks(
            ids=[_chunk_id(chunk, index) for chunk, index in zip(batch, chunk_indices)],
            embeddings=vectors,
            documents=[chunk.text for chunk in batch],
            sources=[chunk.source for chunk in batch],
            pages=[chunk.page for chunk in batch],
            chunk_indices=chunk_indices,
        )
        logger.info(
            "build_index_batch_upserted",
            start=start,
            end=min(start + UPSERT_BATCH_SIZE, total),  
        )

    logger.info(
        "build_index_completed",
        total_chunks=total,
        collection_count=collection_count(),
    )


if __name__ == "__main__":
    build_index()





