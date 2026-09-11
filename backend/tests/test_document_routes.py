from fastapi.testclient import TestClient

from app.api.routes import document_routes
from app.documents.ingestion import DocumentDeletionResult, DocumentIngestionResult
from app.main import app


def test_upload_endpoint_saves_and_indexes_multiple_pdfs(monkeypatch, tmp_path):
    monkeypatch.setattr(document_routes.settings, "books_path", tmp_path)
    monkeypatch.setattr(
        document_routes,
        "ingest_pdf",
        lambda pdf_path, source, force: DocumentIngestionResult(
            source=source,
            status="indexed",
            chunks_indexed=3,
            message="Textbook is ready for questions.",
        ),
    )

    client = TestClient(app)
    response = client.post(
        "/api/v1/documents/upload",
        files=[
            ("files", ("biology.pdf", b"%PDF-1.4 biology", "application/pdf")),
            ("files", ("chemistry.pdf", b"%PDF-1.4 chemistry", "application/pdf")),
        ],
    )

    assert response.status_code == 200
    assert [item["status"] for item in response.json()["documents"]] == ["indexed", "indexed"]
    assert (tmp_path / "uploads" / "biology.pdf").read_bytes() == b"%PDF-1.4 biology"
    assert (tmp_path / "uploads" / "chemistry.pdf").read_bytes() == b"%PDF-1.4 chemistry"
    assert [item["source"] for item in response.json()["documents"]] == [
        "uploads/biology.pdf",
        "uploads/chemistry.pdf",
    ]


def test_upload_endpoint_rejects_non_pdf_files():
    client = TestClient(app)
    response = client.post(
        "/api/v1/documents/upload",
        files={"files": ("notes.txt", b"not a PDF", "text/plain")},
    )

    assert response.status_code == 400
    assert "Only files" in response.json()["detail"]


def test_delete_upload_endpoint_removes_student_uploaded_book(monkeypatch):
    monkeypatch.setattr(
        document_routes,
        "delete_uploaded_document",
        lambda filename: DocumentDeletionResult(
            source=f"uploads/{filename}",
            chunks_removed=4,
            message="The uploaded textbook and its searchable passages were removed.",
        ),
    )

    client = TestClient(app)
    response = client.delete("/api/v1/documents/uploads/biology.pdf")

    assert response.status_code == 200
    assert response.json() == {
        "source": "uploads/biology.pdf",
        "chunks_removed": 4,
        "message": "The uploaded textbook and its searchable passages were removed.",
    }
