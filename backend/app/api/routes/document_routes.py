"""Endpoints for adding PDF textbooks without code changes."""
from __future__ import annotations

from pathlib import Path
import re
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.documents.ingestion import document_status, ingest_pdf
from app.schemas.document_schema import (
    DocumentIngestionResponse,
    DocumentStatusResponse,
    DocumentUploadResponse,
)


router = APIRouter()
MAX_PDF_SIZE_BYTES = 100 * 1024 * 1024
_INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _safe_pdf_filename(filename: str | None) -> str:
    candidate = _INVALID_FILENAME_CHARACTERS.sub("_", Path(filename or "textbook.pdf").name)
    if not candidate or candidate in {".", ".."} or Path(candidate).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only files with a .pdf extension can be added as textbooks.",
        )
    return candidate[:255]


async def _save_upload(file: UploadFile, destination: Path) -> None:
    """Save one upload atomically and enforce a practical per-book limit."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = destination.with_name(f".{destination.name}.{uuid4().hex}.uploading")
    size = 0
    try:
        with temporary_path.open("wb") as output:
            while block := await file.read(1024 * 1024):
                size += len(block)
                if size > MAX_PDF_SIZE_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="Each PDF must be 100 MB or smaller.",
                    )
                output.write(block)
        if size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded PDF is empty.",
            )
        temporary_path.replace(destination)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


@router.get("/status", response_model=DocumentStatusResponse)
def get_document_status() -> DocumentStatusResponse:
    """Show how many textbooks and chunks are ready for student questions."""
    return DocumentStatusResponse(**document_status())


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_textbooks(
    files: list[UploadFile] = File(..., description="One or more PDF textbooks."),
) -> DocumentUploadResponse:
    """Upload and immediately index one or many PDFs.

    The local setup stores selected books in ``Books/uploads`` on this device.
    Uploading a file with the same name replaces its older indexed contents.
    For very large batches, teachers may instead copy PDFs anywhere into the
    ``Books`` folder; the background watcher will process them automatically.
    """
    if not files:
        raise HTTPException(status_code=400, detail="Choose at least one PDF.")

    results: list[DocumentIngestionResponse] = []
    for file in files:
        filename = _safe_pdf_filename(file.filename)
        upload_directory = settings.books_path / "uploads"
        destination = upload_directory / filename
        await _save_upload(file, destination)
        source = destination.relative_to(settings.books_path).as_posix()
        result = ingest_pdf(destination, source=source, force=True)
        results.append(DocumentIngestionResponse(**result.as_dict()))

    return DocumentUploadResponse(documents=results)
