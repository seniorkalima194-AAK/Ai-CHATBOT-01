from app.documents import ingestion
from vector_db import store


def _vector() -> list[float]:
    return [0.0] * store.EXPECTED_DIM


def test_replace_source_chunks_removes_the_previous_version(monkeypatch, tmp_path):
    monkeypatch.setattr(store, "INDEX_FILE", tmp_path / "index.json")
    store.upsert_chunks(
        ids=["old-biology", "chemistry"],
        embeddings=[_vector(), _vector()],
        documents=["old biology", "chemistry"],
        sources=["biology.pdf", "chemistry.pdf"],
        pages=[1, 1],
        chunk_indices=[0, 0],
    )

    store.replace_source_chunks(
        source="biology.pdf",
        ids=["new-biology-1", "new-biology-2"],
        embeddings=[_vector(), _vector()],
        documents=["new biology one", "new biology two"],
        pages=[1, 2],
        chunk_indices=[0, 0],
    )

    records = {record["id"]: record for record in store.load_records()}
    assert set(records) == {"chemistry", "new-biology-1", "new-biology-2"}
    assert store.index_summary() == {"chunks": 3, "sources": 2}


def test_process_pdf_keeps_chunks_from_every_page(monkeypatch, tmp_path):
    pdf_path = tmp_path / "biology.pdf"
    pdf_path.write_bytes(b"placeholder PDF")
    monkeypatch.setattr(
        ingestion,
        "extract_pdf",
        lambda _path: [
            {"page": 1, "text": "First biology page."},
            {"page": 2, "text": "Second biology page."},
        ],
    )
    monkeypatch.setattr(ingestion, "clean_text", lambda text: text)
    monkeypatch.setattr(ingestion, "chunk_text", lambda text, **_kwargs: [text])

    chunks = ingestion.process_pdf(pdf_path)

    assert chunks == [
        {"text": "First biology page.", "source": "biology.pdf", "page": 1},
        {"text": "Second biology page.", "source": "biology.pdf", "page": 2},
    ]


def test_delete_uploaded_document_removes_its_pdf_index_and_manifest(monkeypatch, tmp_path):
    books_dir = tmp_path / "Books"
    upload_directory = books_dir / "uploads"
    upload_directory.mkdir(parents=True)
    pdf_path = upload_directory / "student-notes.pdf"
    pdf_path.write_bytes(b"PDF")
    manifest_path = tmp_path / "processed" / "manifest.json"
    manifest_path.parent.mkdir()
    manifest_path.write_text(
        '{"uploads/student-notes.pdf": {"status": "indexed", "chunks_indexed": 1}}',
        encoding="utf-8",
    )
    monkeypatch.setattr(ingestion, "BOOKS_DIR", books_dir)
    monkeypatch.setattr(ingestion, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(store, "INDEX_FILE", tmp_path / "index.json")
    store.upsert_chunks(
        ids=["student", "shared"],
        embeddings=[_vector(), _vector()],
        documents=["student content", "shared content"],
        sources=["uploads/student-notes.pdf", "biology.pdf"],
        pages=[1, 1],
        chunk_indices=[0, 0],
    )

    result = ingestion.delete_uploaded_document("student-notes.pdf")

    assert result.source == "uploads/student-notes.pdf"
    assert result.chunks_removed == 1
    assert not pdf_path.exists()
    assert [record["id"] for record in store.load_records()] == ["shared"]
    assert "student-notes.pdf" not in manifest_path.read_text(encoding="utf-8")


def test_list_uploaded_documents_does_not_include_shared_books(monkeypatch, tmp_path):
    books_dir = tmp_path / "Books"
    upload_directory = books_dir / "uploads"
    upload_directory.mkdir(parents=True)
    (upload_directory / "student.pdf").write_bytes(b"PDF")
    (books_dir / "teacher.pdf").write_bytes(b"PDF")
    manifest_path = tmp_path / "processed" / "manifest.json"
    manifest_path.parent.mkdir()
    manifest_path.write_text(
        '{"uploads/student.pdf": {"status": "indexed", "chunks_indexed": 2}}',
        encoding="utf-8",
    )
    monkeypatch.setattr(ingestion, "BOOKS_DIR", books_dir)
    monkeypatch.setattr(ingestion, "MANIFEST_PATH", manifest_path)

    assert ingestion.list_uploaded_documents() == [
        {
            "filename": "student.pdf",
            "source": "uploads/student.pdf",
            "status": "indexed",
            "chunks_indexed": 2,
        }
    ]


def test_ingest_pending_documents_indexes_new_pdf_then_skips_it(monkeypatch, tmp_path):
    books_dir = tmp_path / "Books"
    processed_dir = tmp_path / "processed"
    pdf_path = books_dir / "biology.pdf"
    books_dir.mkdir()
    pdf_path.write_bytes(b"placeholder PDF")

    monkeypatch.setattr(ingestion, "BOOKS_DIR", books_dir)
    monkeypatch.setattr(ingestion, "MANIFEST_PATH", processed_dir / "manifest.json")
    monkeypatch.setattr(
        ingestion,
        "process_pdf",
        lambda _path, source: [{"text": "Biology studies life.", "source": source, "page": 1}],
    )
    monkeypatch.setattr(ingestion, "embed_batch", lambda texts: [_vector() for _ in texts])
    captured: dict[str, object] = {}
    monkeypatch.setattr(
        ingestion,
        "replace_source_chunks",
        lambda **kwargs: captured.update(kwargs),
    )

    first_result = ingestion.ingest_pending_documents()
    second_result = ingestion.ingest_pending_documents()

    assert first_result[0].status == "indexed"
    assert first_result[0].chunks_indexed == 1
    assert second_result[0].status == "skipped"
    assert captured["source"] == "biology.pdf"
    assert captured["documents"] == ["Biology studies life."]


def test_document_status_reports_ready_books(monkeypatch, tmp_path):
    books_dir = tmp_path / "Books"
    books_dir.mkdir()
    (books_dir / "book.pdf").write_bytes(b"PDF")
    manifest_path = tmp_path / "processed" / "manifest.json"
    manifest_path.parent.mkdir()
    manifest_path.write_text(
        '{"book.pdf": {"status": "indexed", "chunks_indexed": 2}}', encoding="utf-8"
    )
    monkeypatch.setattr(ingestion, "BOOKS_DIR", books_dir)
    monkeypatch.setattr(ingestion, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(ingestion, "index_summary", lambda: {"chunks": 12, "sources": 3})

    assert ingestion.document_status() == {
        "chunks": 12,
        "sources": 3,
        "pdf_files": 1,
        "indexed_files": 1,
    }
