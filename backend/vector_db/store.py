"""
vector_db/store.py

Owns the Chroma persistent client and collection, and write-side
operations (upsert / count / reset) only.

Scope boundary (per issue #6, explicitly): similarity search / querying
belongs to rag/retriever.py, NOT here. This module never calls
`.query()`. If you find yourself adding a search function to this file,
that's scope creep back into the retrieval module's job.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Sequence

import chromadb

try:
    from chromadb.api.models.Collection import Collection
except ImportError:
    # chromadb has moved this internal path across versions before.
    # Only used for type hints — falling back to Any keeps this module
    # importable even if that internal path changes again. This is the
    # exact kind of version fragility flagged earlier: pin chromadb's
    # version in requirements.txt, don't rely on this fallback silently
    # covering for an upgrade you didn't test.
    Collection = Any  # type: ignore

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# DESIGN DECISION — confirm or override:
# Persisted Chroma data (sqlite + parquet index files) lives in a
# subdirectory, NOT directly in vector_db/ next to this .py file. Reasons:
#   1. .gitignore stays simple — ignore chroma_data/ wholesale, store.py
#      (source code) still gets committed normally.
#   2. Chroma writes many binary files; mixing them with tracked source
#      files in the same dir is a mess to review in PRs.
# If your issue literally meant "the Chroma persist path IS vector_db/",
# override with the VECTOR_DB_PATH env var — don't just edit this constant
# and lose the override mechanism.
DEFAULT_PERSIST_DIR = Path(__file__).resolve().parent / "chroma_data"
PERSIST_DIR = Path(os.environ.get("VECTOR_DB_PATH", str(DEFAULT_PERSIST_DIR)))

COLLECTION_NAME = "course_materials"

# all-MiniLM-L6-v2 output size. embeddings.py is the source of truth for
# the actual model; this constant exists ONLY so a dimension mismatch
# fails loudly and immediately here, instead of surfacing later as a
# cryptic Chroma internal error or — worse — silently degraded retrieval.
EXPECTED_DIM = 384


# --------------------------------------------------------------------------
# Client / collection
# --------------------------------------------------------------------------

_client: chromadb.PersistentClient | None = None


def get_client() -> chromadb.PersistentClient:
    """Singleton persistent Chroma client rooted at PERSIST_DIR."""
    global _client
    if _client is None:
        PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    return _client


def get_collection() -> Collection:
    """
    Get or create the collection used for course-material chunks.

    embedding_function=None is deliberate, not an oversight: embeddings.py
    owns the model (all-MiniLM-L6-v2) and passes vectors in explicitly on
    every write. If this collection were created WITHOUT that override,
    Chroma falls back to its own default embedding function on first use —
    which downloads a different local model the first time it's called.
    That breaks the offline guarantee for a machine that's never had
    embeddings.py's model cached, and it means you now have two disagreeing
    embedding spaces in one project. Do not remove this argument.

    hnsw:space=cosine is set explicitly rather than left as Chroma's
    default — confirm this matches whatever similarity metric
    retriever.py assumes when it queries this collection. A mismatch
    between what's set here and what retriever.py expects is a silent
    relevance bug, not a crash.
    """
    client = get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )


# --------------------------------------------------------------------------
# ID scheme — this IS the idempotency requirement from the issue
# --------------------------------------------------------------------------

def make_chunk_id(source: str, page: int, chunk_index: int) -> str:
    """
    Deterministic ID for one chunk: composite of (source, page,
    chunk_index) — deliberately NOT a hash of the chunk text.

    Hashing text alone collides whenever two different chunks share
    boilerplate (headers, footers, repeated formulas across a syllabus).
    source+page alone collides whenever a page produces more than one
    chunk, which it will for any chunk size smaller than a full page.

    This ID is what makes build_index.py idempotent: re-running it on the
    same source material produces the same IDs, so upsert() overwrites in
    place instead of duplicating. It stops being stable only if the
    chunking logic itself changes (different chunk_size/overlap producing
    a different chunk_index for the same text) — that's expected; changing
    the chunking strategy SHOULD be treated as a fresh index, not a
    seamless re-run.
    """
    raw = f"{source}::{page}::{chunk_index}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


# --------------------------------------------------------------------------
# Write operations
# --------------------------------------------------------------------------

def upsert_chunks(
    ids: Sequence[str],
    embeddings: Sequence[Sequence[float]],
    documents: Sequence[str],
    sources: Sequence[str],
    pages: Sequence[int],
    chunk_indices: Sequence[int],
) -> None:
    """
    Upsert (never add) a batch of chunks.

    Using upsert instead of add is the actual mechanism behind the
    "re-running should not duplicate" acceptance criterion — it isn't
    handled anywhere else, so it has to be handled here.

    chunk_index is stored as its own metadata field (not just folded into
    the ID) so retriever.py can reconstruct which specific passage on a
    page was matched, not just which page — the issue's stated schema
    (vector + text + source + page) under-specifies this; two chunks on
    the same page are otherwise indistinguishable in the returned
    metadata.

    All arguments must be equal length; raises ValueError immediately on
    mismatch or on any embedding whose dimension isn't EXPECTED_DIM,
    rather than letting a malformed batch fail deep inside Chroma with a
    less diagnosable error.
    """
    n = len(ids)
    lengths = {
        "ids": n,
        "embeddings": len(embeddings),
        "documents": len(documents),
        "sources": len(sources),
        "pages": len(pages),
        "chunk_indices": len(chunk_indices),
    }
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Mismatched batch lengths: {lengths}")
    if n == 0:
        return

    for i, vec in enumerate(embeddings):
        if len(vec) != EXPECTED_DIM:
            raise ValueError(
                f"Embedding at batch index {i} has dimension {len(vec)}, "
                f"expected {EXPECTED_DIM}. Check embeddings.py is still "
                f"using all-MiniLM-L6-v2 and hasn't been swapped for a "
                f"different model without updating this constant."
            )

    metadatas = [
        {"source": src, "page": page, "chunk_index": idx}
        for src, page, idx in zip(sources, pages, chunk_indices)
    ]

    collection = get_collection()
    collection.upsert(
        ids=list(ids),
        embeddings=[list(e) for e in embeddings],
        documents=list(documents),
        metadatas=metadatas,
    )


# --------------------------------------------------------------------------
# Introspection — for build_index.py logging and idempotency tests
# --------------------------------------------------------------------------

def count() -> int:
    """Chunks currently stored. Log this before and after build_index.py
    runs — the acceptance criterion is that a re-run leaves this number
    unchanged, so make that provable, not just assumed."""
    return get_collection().count()


def reset() -> None:
    """
    Delete the entire collection. Destructive — for tests and deliberate
    full rebuilds only (e.g. after a chunking-strategy change, per the
    note in make_chunk_id). Does NOT delete PERSIST_DIR itself.
    """
    client = get_client()
    client.delete_collection(name=COLLECTION_NAME)


if __name__ == "__main__":
    # Manual smoke test only — confirms the store can be created and
    # written to without needing embeddings.py or a real PDF wired up yet.
    # Not a substitute for tests/test_retrieval.py.
    print(f"Persist dir: {PERSIST_DIR}")
    dummy_vec = [0.0] * EXPECTED_DIM
    cid = make_chunk_id("smoke_test.pdf", 1, 0)
    upsert_chunks(
        ids=[cid],
        embeddings=[dummy_vec],
        documents=["smoke test chunk"],
        sources=["smoke_test.pdf"],
        pages=[1],
        chunk_indices=[0],
    )
    print(f"Collection count after smoke test upsert: {count()}")
    print("Re-run this script — count should stay at 1, not grow to 2.")
