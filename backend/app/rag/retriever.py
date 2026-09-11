"""Read-side similarity retrieval for the local educational knowledge base."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from app.core.config import settings
from app.core.logging import logger
from app.rag.embeddings import embed_query
from vector_db.store import COLLECTION_NAME, load_records


@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float
    metadata: dict[str, Any]


class Retriever:
    """Ranks locally stored normalized vectors using cosine similarity."""

    COLLECTION_NAME = COLLECTION_NAME

    def __init__(
        self,
        vector_db_path: Optional[Path] = None,
        top_k: Optional[int] = None,
    ) -> None:
        self.vector_db_path = Path(vector_db_path or settings.vector_db_path)
        self.top_k = top_k if top_k is not None else settings.top_k
        logger.info(
            "retriever_ready",
            path=str(self.vector_db_path),
            collection=self.COLLECTION_NAME,
            document_count=len(load_records()),
            top_k=self.top_k,
        )

    def retrieve(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> list[RetrievedChunk]:
        k = top_k if top_k is not None else self.top_k
        if k <= 0:
            return []

        records = load_records()
        if not records:
            logger.warning("vector_store_empty", path=str(self.vector_db_path))
            return []

        query_embedding = embed_query(question)

        def score(record: dict[str, Any]) -> float:
            return sum(
                left * right
                for left, right in zip(query_embedding, record["embedding"])
            )

        ranked = sorted(records, key=score, reverse=True)[:k]
        chunks = []
        for record in ranked:
            document = str(record.get("document", "")).strip()
            if not document:
                continue
            metadata = dict(record.get("metadata") or {})
            chunks.append(
                RetrievedChunk(
                    text=document,
                    source=str(metadata.get("source", "unknown")),
                    score=score(record),
                    metadata=metadata,
                )
            )

        logger.info(
            "retrieval_complete",
            question_preview=question[:80],
            returned=len(chunks),
            top_score=round(chunks[0].score, 4) if chunks else None,
        )
        return chunks
