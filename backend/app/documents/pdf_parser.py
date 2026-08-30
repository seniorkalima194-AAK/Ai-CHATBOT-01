# Placeholder: PDF parsing utility for educational documents.
from pathlib import Path
import logging

from pypdf import PdfReader


logger = logging.getLogger(__name__)


def extract_pdf(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from a PDF document.

    Each page returns:
        - text
        - page
        - source
    """

    pdf_path = Path(pdf_path)

    pages = []

    try:
        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(reader.pages, start=1):

            try:
                text = page.extract_text() or ""
                text = text.strip()

            except Exception as error:
                logger.warning(
                    "Failed to extract page %s from %s: %s",
                    page_number,
                    pdf_path.name,
                    error,
                )
                continue

            if not text:
                logger.warning(
                    "No text found on page %s of %s",
                    page_number,
                    pdf_path.name,
                )
                continue

            pages.append(
                {
                    "text": text,
                    "page": page_number,
                    "source": pdf_path.name,
                }
            )

    except Exception as error:
        logger.warning(
            "Failed to open PDF %s: %s",
            pdf_path,
            error,
        )

    return pages