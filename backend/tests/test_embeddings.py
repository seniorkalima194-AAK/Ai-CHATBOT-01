"""
Unit tests for app/rag/embeddings.py, plus the idempotency guarantee
of scripts/build_index.py's chunk-id logic.

Uses a fake, deterministic embedding model instead of the real
sentence-transformers download — these tests must run offline and fast,
without needing a model pulled first.
"""
from __future__ import annotations

import numpy as np
import pytest

from app.rag import embeddings
from app.schemas.vector_schema import Chunk
from scripts.build_index import _chunk_id


class _FakeModel:
    """Deterministic stand-in: same text always -> same vector."""

    DIM = 384

    def get_sentence_embedding_dimension(self) -> int:
        return self.DIM

    def encode(self, texts, batch_size=32, convert_to_numpy=True,
            normalize_embeddings=True, show_progress_bar=False):
        single = isinstance(texts, str)
        items = [texts] if single else list(texts)
        vectors = np.array(
            [np.full(self.DIM, (hash(t) % 1000) / 1000.0, dtype=np.float32) for t in items]
        )
        return vectors[0] if single else vectors


@pytest.fixture(autouse=True)
def fake_embedding_model(monkeypatch):
    """
    Every test in this file uses the fake model, not the real one.
    Only clear the cache before patching — monkeypatch restores the
    original attribute automatically after the test, so clearing it
    again afterward would run on the fake (already-patched) function,
    which has no cache to clear.
    """
    embeddings._get_model.cache_clear()
    monkeypatch.setattr(embeddings, "_get_model", lambda: _FakeModel())
    yield


# --- embed() / embed_batch() ---

def test_embed_returns_correct_dimension():
    vector = embeddings.embed("What is photosynthesis?")
    assert len(vector) == embeddings.EXPECTED_EMBEDDING_DIM


def test_embed_batch_returns_correct_dimension_for_each_item():
    texts = [f"Sample sentence {i}" for i in range(10)]
    vectors = embeddings.embed_batch(texts)
    assert len(vectors) == 10
    assert all(len(v) == embeddings.EXPECTED_EMBEDDING_DIM for v in vectors)


def test_embed_rejects_empty_string():
    with pytest.raises(ValueError):
        embeddings.embed("   ")


def test_embed_batch_drops_blank_strings():
    result = embeddings.embed_batch(["real text", "", "   "])
    assert len(result) == 1


def test_embed_batch_empty_list_returns_empty_list():
    assert embeddings.embed_batch([]) == []


# --- validate_dimension() ---

def test_validate_dimension_passes_for_correct_model():
    embeddings.validate_dimension()  # should not raise


def test_validate_dimension_raises_on_mismatch(monkeypatch):
    class WrongDimModel(_FakeModel):
        DIM = 768

    monkeypatch.setattr(embeddings, "_get_model", lambda: WrongDimModel())
    with pytest.raises(ValueError, match="768-dim"):
        embeddings.validate_dimension()


# --- idempotency: chunk id generation ---

def test_chunk_id_is_deterministic():
    chunk = Chunk(text="Photosynthesis converts light to energy.", source="bio.pdf", page=12)
    assert _chunk_id(chunk) == _chunk_id(chunk)


def test_chunk_id_differs_for_different_text():
    a = Chunk(text="Text A", source="bio.pdf", page=1)
    b = Chunk(text="Text B", source="bio.pdf", page=1)
    assert _chunk_id(a) != _chunk_id(b)


def test_chunk_id_differs_for_same_text_different_page():
    a = Chunk(text="Same text", source="bio.pdf", page=1)
    b = Chunk(text="Same text", source="bio.pdf", page=2)
    assert _chunk_id(a) != _chunk_id(b)


def test_chunk_id_differs_for_same_text_different_source():
    a = Chunk(text="Same text", source="bio.pdf", page=1)
    b = Chunk(text="Same text", source="chem.pdf", page=1)
    assert _chunk_id(a) != _chunk_id(b)


# --- Chunk schema validation ---

def test_chunk_rejects_blank_text():
    with pytest.raises(Exception):
        Chunk(text="   ", source="bio.pdf", page=1)


def test_chunk_rejects_negative_page():
    with pytest.raises(Exception):
        Chunk(text="Valid text", source="bio.pdf", page=-1)