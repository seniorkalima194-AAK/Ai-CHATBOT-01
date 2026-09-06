"""Manually rebuild the local index from every PDF in ``backend/Books``.

Normally this is unnecessary: the running backend watches the Books folder and
imports new or changed PDFs automatically. This command is useful when a
teacher wants to force a complete refresh immediately.
"""
from __future__ import annotations

from hashlib import sha256

from app.core.logging import get_logger
from app.documents.ingestion import ingest_pending_documents
from app.schemas.vector_schema import Chunk


logger = get_logger(__name__)


def _chunk_id(chunk: Chunk, chunk_index: int = 0) -> str:
    """Return the stable identifier retained for import-tool compatibility."""
    raw = f"{chunk.source}|{chunk.page}|{chunk_index}|{chunk.text}".encode("utf-8")
    return sha256(raw).hexdigest()


def build_index() -> None:
    """Force-reindex the Books library and log a compact result."""
    reports = ingest_pending_documents(force=True)
    indexed = sum(report.status == "indexed" for report in reports)
    failed = sum(report.status == "failed" for report in reports)
    logger.info(
        "books_index_rebuilt",
        total=len(reports),
        indexed=indexed,
        failed=failed,
    )


if __name__ == "__main__":
    build_index()
