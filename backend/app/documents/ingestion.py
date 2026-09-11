"""Automatic, repeatable ingestion of PDF textbooks into the local index."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import threading
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger
from app.documents.chunker import chunk_text
from app.documents.cleaner import clean_text
from app.documents.pdf_parser import extract_pdf
from app.rag.embeddings import embed_batch
from vector_db.store import index_summary, remove_source_chunks, replace_source_chunks


logger = get_logger(__name__)

BOOKS_DIR = settings.books_path
PROCESSED_DIR = settings.processed_documents_path
MANIFEST_PATH = PROCESSED_DIR / "ingestion_manifest.json"
EMBEDDING_BATCH_SIZE = 64
_ingestion_lock = threading.Lock()


@dataclass(frozen=True)
class DocumentIngestionResult:
    """Outcome for one PDF supplied through the folder or upload API."""

    source: str
    status: str
    chunks_indexed: int
    message: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentDeletionResult:
    """Outcome of removing a PDF that was uploaded through the student UI."""

    source: str
    chunks_removed: int
    message: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def process_pdf(pdf_path: Path, source: str | None = None) -> list[dict[str, Any]]:
    """Extract, clean, and chunk one text-based PDF without indexing it yet."""
    source = source or pdf_path.name
    processed_chunks: list[dict[str, Any]] = []

    for page in extract_pdf(pdf_path):
        cleaned = clean_text(page["text"])
        if not cleaned:
            continue

        for text in chunk_text(
            cleaned,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        ):
            processed_chunks.append(
                {"text": text, "source": source, "page": page["page"]}
            )

    return processed_chunks


def _load_manifest() -> dict[str, dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        return {}
    try:
        with MANIFEST_PATH.open("r", encoding="utf-8") as file:
            manifest = json.load(file)
    except (OSError, json.JSONDecodeError):
        logger.warning("ingestion_manifest_unreadable", path=str(MANIFEST_PATH))
        return {}
    return manifest if isinstance(manifest, dict) else {}


def _save_manifest(manifest: dict[str, dict[str, Any]]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = MANIFEST_PATH.with_suffix(f".{os.getpid()}.tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(temporary_path, MANIFEST_PATH)


def _file_signature(pdf_path: Path) -> str:
    """A quick change detector; PDF contents are read only when this changes."""
    stat = pdf_path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def _chunk_id(source: str, page: int, chunk_index: int, text: str) -> str:
    raw = f"{source}|{page}|{chunk_index}|{text}".encode("utf-8")
    return sha256(raw).hexdigest()


def _embed_and_replace(source: str, chunks: list[dict[str, Any]]) -> int:
    texts = [str(chunk["text"]) for chunk in chunks]
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        embeddings.extend(embed_batch(texts[start : start + EMBEDDING_BATCH_SIZE]))

    if len(embeddings) != len(chunks):
        raise RuntimeError("The embedding model did not return one vector per chunk.")

    page_indices: defaultdict[int, int] = defaultdict(int)
    pages: list[int] = []
    chunk_indices: list[int] = []
    ids: list[str] = []
    for chunk in chunks:
        page = int(chunk["page"])
        page_index = page_indices[page]
        page_indices[page] += 1
        pages.append(page)
        chunk_indices.append(page_index)
        ids.append(_chunk_id(source, page, page_index, str(chunk["text"])))

    replace_source_chunks(
        source=source,
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        pages=pages,
        chunk_indices=chunk_indices,
    )
    return len(chunks)


def _ingest_one(
    pdf_path: Path,
    source: str,
    manifest: dict[str, dict[str, Any]],
    *,
    force: bool,
) -> DocumentIngestionResult:
    signature = _file_signature(pdf_path)
    existing = manifest.get(source, {})
    if not force and existing.get("signature") == signature:
        return DocumentIngestionResult(
            source, "skipped", int(existing.get("chunks_indexed", 0)), "Already indexed."
        )

    try:
        chunks = process_pdf(pdf_path, source=source)
        if not chunks:
            result = DocumentIngestionResult(
                source,
                "failed",
                0,
                "No readable text was found. This may be a scanned-image PDF.",
            )
        else:
            chunk_count = _embed_and_replace(source, chunks)
            result = DocumentIngestionResult(
                source, "indexed", chunk_count, "Textbook is ready for questions."
            )
    except Exception as exc:
        logger.exception("document_ingestion_failed", source=source)
        result = DocumentIngestionResult(source, "failed", 0, str(exc))

    manifest[source] = {
        "signature": signature,
        "chunks_indexed": result.chunks_indexed,
        "status": result.status,
    }
    return result


def ingest_pdf(pdf_path: Path, source: str | None = None, *, force: bool = False) -> DocumentIngestionResult:
    """Index a single PDF now, replacing old chunks when its name matches."""
    pdf_path = Path(pdf_path)
    source = source or pdf_path.name
    with _ingestion_lock:
        manifest = _load_manifest()
        result = _ingest_one(pdf_path, source, manifest, force=force)
        _save_manifest(manifest)
        return result


def list_uploaded_documents() -> list[dict[str, Any]]:
    """List PDFs saved by the student upload UI, never the shared library."""
    upload_directory = BOOKS_DIR / "uploads"
    if not upload_directory.exists():
        return []

    manifest = _load_manifest()
    documents: list[dict[str, Any]] = []
    for pdf_path in sorted(upload_directory.glob("*.pdf"), key=lambda path: path.name.lower()):
        source = pdf_path.relative_to(BOOKS_DIR).as_posix()
        record = manifest.get(source, {})
        documents.append(
            {
                "filename": pdf_path.name,
                "source": source,
                "status": str(record.get("status", "pending")),
                "chunks_indexed": int(record.get("chunks_indexed", 0)),
            }
        )
    return documents


def delete_uploaded_document(filename: str) -> DocumentDeletionResult:
    """Delete one student-uploaded PDF and all knowledge indexed from it."""
    upload_directory = BOOKS_DIR / "uploads"
    pdf_path = upload_directory / filename
    if pdf_path.parent != upload_directory or not pdf_path.is_file():
        raise FileNotFoundError(filename)

    source = pdf_path.relative_to(BOOKS_DIR).as_posix()
    with _ingestion_lock:
        # Delete the PDF before its vectors. If Windows has the file open, the
        # deletion fails and the AI keeps the existing knowledge unchanged.
        pdf_path.unlink()
        chunks_removed = remove_source_chunks(source)
        manifest = _load_manifest()
        manifest.pop(source, None)
        _save_manifest(manifest)

    return DocumentDeletionResult(
        source=source,
        chunks_removed=chunks_removed,
        message="The uploaded textbook and its searchable passages were removed.",
    )


def _book_pdf_paths() -> list[Path]:
    """Return PDFs in the shared Books library, including subfolders."""
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(
        path for path in BOOKS_DIR.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf"
    )


def ingest_pending_documents(*, force: bool = False) -> list[DocumentIngestionResult]:
    """Index new or changed PDFs dropped anywhere in the ``Books`` folder.

    Nested folders are supported. A file is only processed again when its size
    or modification time changes, so a folder with hundreds of books is cheap
    to scan after its initial import.
    """
    pdf_paths = _book_pdf_paths()

    with _ingestion_lock:
        manifest = _load_manifest()
        results = []
        for pdf_path in pdf_paths:
            source = pdf_path.relative_to(BOOKS_DIR).as_posix()
            results.append(_ingest_one(pdf_path, source, manifest, force=force))
            # A large school library can take a while to import. Persist each
            # completed book so an interruption never loses all progress.
            _save_manifest(manifest)
        return results


def document_status() -> dict[str, int]:
    """Return counts for administrators or the future management screen."""
    pdf_paths = _book_pdf_paths()
    sources = {path.relative_to(BOOKS_DIR).as_posix() for path in pdf_paths}
    manifest = _load_manifest()
    return {
        **index_summary(),
        "pdf_files": len(pdf_paths),
        "indexed_files": sum(
            1
            for source in sources
            if manifest.get(source, {}).get("status") == "indexed"
        ),
    }


def ingest_documents() -> list[DocumentIngestionResult]:
    """Backward-compatible command entry point that force-rebuilds the folder."""
    return ingest_pending_documents(force=True)


if __name__ == "__main__":
    for report in ingest_pending_documents():
        print(report.as_dict())
