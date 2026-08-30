# Placeholder: retrieval logic for fetching relevant context from the vector store.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.core.logging import logger
from app.rag.embeddings import embed_query

#hii hutumika kubeba matokeo ya utafutaji kwenye RAG pipeline 
@dataclass
class RetrievedChunk:
    """One retrieved context chunk with source metadata."""

    text: str
    source: str
    score: float
    metadata: Dict[str, Any]

#hii hupokea swali la mtumiaji na kubadilisha kuwa embedding vector, 
class Retriever:
    """
    Runs cosine similarity search against the persistent Chroma collection
    and returns the top-k chunks together with their source metadata.
    """

    COLLECTION_NAME = "educational_materials"

    def __init__(
        self,
        vector_db_path: Optional[Path] = None,
        top_k: Optional[int] = None,
    ) -> None:
        self.vector_db_path = Path(vector_db_path or settings.vector_db_path)
        self.top_k = top_k if top_k is not None else settings.top_k

        self._client = chromadb.PersistentClient(
            path=str(self.vector_db_path),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

        logger.info(
            "retriever_ready",
            path=str(self.vector_db_path),
            collection=self.COLLECTION_NAME,
            document_count=self._collection.count(),
            top_k=self.top_k,
        )

    def retrieve(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> List[RetrievedChunk]:
        """
        Embed the question and return the most similar chunks.

        Each chunk carries:
        - text
        - source (filename / document title)
        - similarity score (higher = better)
        - original metadata
        """
        k = top_k if top_k is not None else self.top_k
        if k <= 0:
            return []

        count = self._collection.count()
        if count == 0:
            logger.warning("vector_store_empty", path=str(self.vector_db_path))
            return []

        query_embedding = embed_query(question)

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, count),
            include=["documents", "metadatas", "distances"],
        )

        documents = (results.get("documents") or [[]])[0]
        metadatas = (results.get("metadatas") or [[]])[0]
        distances = (results.get("distances") or [[]])[0]

        chunks: List[RetrievedChunk] = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            if not doc:
                continue

            # Chroma distance → similarity score (1.0 = perfect match)
            score = 1.0 - float(dist) if dist is not None else 0.0
            meta = meta or {}
            source = (
                meta.get("source")
                or meta.get("filename")
                or meta.get("document")
                or "unknown"
            )

            chunks.append(
                RetrievedChunk(
                    text=doc.strip(),
                    source=str(source),
                    score=score,
                    metadata=dict(meta),
                )
            )

        logger.info(
            "retrieval_complete",
            question_preview=question[:80],
            returned=len(chunks),
            top_score=round(chunks[0].score, 4) if chunks else None,
        )
        return chunks