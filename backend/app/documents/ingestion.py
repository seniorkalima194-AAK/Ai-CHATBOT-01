# Placeholder: ingestion workflow for processing and indexing documents.
from pathlib import Path
import json
import logging

from app.documents.pdf_parser import extract_pdf
from app.documents.cleaner import clean_text
from app.documents.chunker import chunk_text
from app.core.config import settings


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RAW_DIR = settings.raw_documents_path

PROCESSED_DIR = settings.processed_documents_path

CHUNK_SIZE = settings.chunk_size

CHUNK_OVERLAP = settings.chunk_overlap


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# PROCESS ONE PDF
# --------------------------------------------------

def process_pdf(pdf_path: Path) -> list[dict]:

    logger.info(
        "Processing document: %s",
        pdf_path.name,
    )

    pages = extract_pdf(pdf_path)

    processed_chunks = []

    for page in pages:

        # ------------------------------------------
        # CLEAN TEXT
        # ------------------------------------------

        cleaned = clean_text(
            page["text"]
        )

        if not cleaned:
            logger.warning(
                "Empty page %s in %s",
                page["page"],
                page["source"],
            )

            continue

        # ------------------------------------------
        # CREATE CHUNKS
        # ------------------------------------------

        chunks = chunk_text(
            cleaned,
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP,
        )

        # ------------------------------------------
        # STORE CHUNKS
        # ------------------------------------------

        for chunk in chunks:

            processed_chunks.append(
                {
                    "text": chunk,
                    "source": page["source"],
                    "page": page["page"],
                }
            )

    return processed_chunks


# --------------------------------------------------
# PROCESS ALL PDFs
# --------------------------------------------------

def ingest_documents():

    # Create output directory
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Check input directory
    if not RAW_DIR.exists():

        logger.error(
            "Input directory does not exist: %s",
            RAW_DIR,
        )

        return

    # Find PDFs
    pdf_files = list(
        RAW_DIR.glob("*.pdf")
    )

    if not pdf_files:

        logger.warning(
            "No PDF files found in %s",
            RAW_DIR,
        )

        return

    logger.info(
        "Found %s PDF file(s)",
        len(pdf_files),
    )

    # ------------------------------------------
    # PROCESS EACH PDF
    # ------------------------------------------

    for pdf_path in pdf_files:

        try:

            chunks = process_pdf(
                pdf_path
            )

            if not chunks:

                logger.warning(
                    "No chunks generated for %s",
                    pdf_path.name,
                )

                continue

            # Output filename
            output_file = (
                PROCESSED_DIR
                / f"{pdf_path.stem}.jsonl"
            )

            # Save JSON
            with open(
                output_file,
                "w",
                encoding="utf-8",
            ) as file:

                for chunk in chunks:
                    file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

            logger.info(
                "Successfully saved %s chunks -> %s",
                len(chunks),
                output_file,
            )

        except Exception as error:

            logger.error(
                "Failed to process %s: %s",
                pdf_path.name,
                error,
            )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    ingest_documents()
