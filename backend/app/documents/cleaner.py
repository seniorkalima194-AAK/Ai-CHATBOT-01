# Placeholder: text cleaning and normalization for uploaded documents.
import re

#kusanikinisha maneno kutoka kwenye pdf
def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    Removes:
    - excessive whitespace
    - broken line wrapping
    - standalone page numbers
    """

    # kuunganisha mistari tofauti tofauti kuwa na format moja
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # kuondoa namba za kurasa 
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)

    # Join words broken by a hyphen at line end
    text = re.sub(r"-\n(?=\w)", "", text)

    # Replace newlines between normal words with spaces
    text = re.sub(r"(?<![.!?:])\n(?!\n)", " ", text)

    # Preserve paragraph breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()