# Placeholder: text cleaning and normalization for uploaded documents.
import re


_MOJIBAKE_MARKERS = ("Ã", "Â", "â", "ð", "ï")


def _windows_mojibake_bytes(text: str) -> bytes:
    """Encode CP-1252 text while preserving its five undefined byte slots."""
    result = bytearray()
    for character in text:
        codepoint = ord(character)
        # PDF extractors occasionally retain one of these as a C1 control
        # character. CP-1252 refuses to encode them, although they represent
        # the original byte and are needed to repair strings such as â€.
        if codepoint in {0x81, 0x8D, 0x8F, 0x90, 0x9D}:
            result.append(codepoint)
        else:
            result.extend(character.encode("cp1252"))
    return bytes(result)


def repair_text_encoding(text: str) -> str:
    """Repair common UTF-8-as-Latin-1 corruption found in old PDF indexes.

    Existing biology chunks contain values such as ``â€œ`` and ``ïƒ˜``.  They
    are valid Python strings but make the context, sources, and consequently
    the model's response difficult for a student to read.  New PDFs are
    normalised during ingestion; this helper also lets us repair the existing
    index at read time without changing the trained data in place.
    """
    repaired = text or ""
    for _ in range(2):
        if not any(marker in repaired for marker in _MOJIBAKE_MARKERS):
            break
        try:
            # Windows PDF tools commonly turn UTF-8 bytes into CP-1252
            # characters (for example, â€œ instead of “).
            candidate = _windows_mojibake_bytes(repaired).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
        if candidate == repaired:
            break
        repaired = candidate

    # Some PDFs use a private-use font glyph in place of a bullet point.
    return repaired.replace("\uf0d8", "•")

#kusanikinisha maneno kutoka kwenye pdf
def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.

    Removes:
    - excessive whitespace
    - broken line wrapping
    - standalone page numbers
    """

    text = repair_text_encoding(text)

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
