# Placeholder: embedding generation logic for vector search.

from __future__ import annotations

from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

from app.core.logging import logger
from app.core.config import settings



@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once per process."""
    logger.info("loading_embedding_model", model=DEFAULT_MODEL_NAME)
    model = SentenceTransformer(DEFAULT_MODEL_NAME)
    dim = model.get_embedding_dimension()
    logger.info("embedding_model_ready", model=DEFAULT_MODEL_NAME, dimension=dim)
    return model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed multiple texts. Returns plain Python lists of floats."""
    if not texts:
        return []
    model = get_embedding_model()
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single student question."""
    return embed_texts([query.strip()])[0]