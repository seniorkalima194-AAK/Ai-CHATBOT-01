"""Embedding generation kept separate from application configuration."""
from __future__ import annotations

import hashlib
import math
import re
from functools import lru_cache
from typing import Sequence

from app.core.config import settings
from app.core.logging import logger

EXPECTED_EMBEDDING_DIM = 384


class HashingEmbedder:
    """Small dependency-free fallback for offline retrieval when Torch is unavailable.

    It is less semantic than Sentence Transformers, but it preserves the PDF RAG
    pipeline instead of making the whole service unavailable on a broken native
    PyTorch installation.
    """

    def get_sentence_embedding_dimension(self) -> int:
        return EXPECTED_EMBEDDING_DIM

    def encode(self, texts, **_kwargs):
        return [_hash_embedding(text) for text in texts]


def _hash_embedding(text: str) -> list[float]:
    vector = [0.0] * EXPECTED_EMBEDDING_DIM
    for token in re.findall(r"[\w'-]+", text.lower()):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest[:4], "big") % EXPECTED_EMBEDDING_DIM
        vector[bucket] += 1.0 if digest[4] % 2 else -1.0
    magnitude = math.sqrt(sum(value * value for value in vector))
    return [value / magnitude for value in vector] if magnitude else vector


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only when indexing or searching is needed."""
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("loading_embedding_model", model=settings.embedding_model_name)
        model = SentenceTransformer(settings.embedding_model_name)
    except Exception as exc:
        logger.warning(
            "embedding_model_unavailable_using_hash_fallback",
            model=settings.embedding_model_name,
            error=str(exc),
        )
        return HashingEmbedder()

    logger.info(
        "embedding_model_ready",
        model=settings.embedding_model_name,
        dimension=_dimension(model),
    )
    return model


def _dimension(model) -> int:
    if hasattr(model, "get_sentence_embedding_dimension"):
        return int(model.get_sentence_embedding_dimension())
    return int(model.get_embedding_dimension())


def validate_dimension() -> None:
    dimension = _dimension(get_embedding_model())
    if dimension != EXPECTED_EMBEDDING_DIM:
        raise ValueError(
            f"Embedding model returns {dimension}-dim vectors; expected "
            f"{EXPECTED_EMBEDDING_DIM}."
        )


def embed_texts(texts: Sequence[str]) -> list[list[float]]:
    cleaned = [text.strip() for text in texts if text and text.strip()]
    if not cleaned:
        return []
    vectors = get_embedding_model().encode(
        cleaned,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def embed_query(query: str) -> list[float]:
    vectors = embed_texts([query])
    if not vectors:
        raise ValueError("Question cannot be empty.")
    return vectors[0]


def embed(text: str) -> list[float]:
    return embed_query(text)


def embed_batch(texts: Sequence[str]) -> list[list[float]]:
    return embed_texts(texts)
