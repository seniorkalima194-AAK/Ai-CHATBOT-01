"""Background watcher for textbooks placed in the knowledge folder."""
from __future__ import annotations

import threading

from app.core.config import settings
from app.core.logging import get_logger
from app.documents.ingestion import ingest_pending_documents


logger = get_logger(__name__)


class DocumentWatcher:
    """Periodically index new or changed PDFs without blocking the chat API."""

    def __init__(self, interval_seconds: float | None = None) -> None:
        self.interval_seconds = interval_seconds or settings.document_scan_interval_seconds
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="textbook-indexer",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                results = ingest_pending_documents()
                indexed = sum(result.status == "indexed" for result in results)
                if indexed:
                    logger.info("textbook_folder_indexed", indexed=indexed)
            except Exception:
                logger.exception("textbook_folder_scan_failed")
            self._stop_event.wait(self.interval_seconds)


_default_watcher: DocumentWatcher | None = None


def start_document_watcher() -> None:
    global _default_watcher
    if _default_watcher is None:
        _default_watcher = DocumentWatcher()
    _default_watcher.start()


def stop_document_watcher() -> None:
    if _default_watcher is not None:
        _default_watcher.stop()
