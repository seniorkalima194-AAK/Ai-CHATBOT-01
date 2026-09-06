"""Text cleaning and normalization for uploaded documents."""
import re


_MOJIBAKE_MARKERS = ("\u00c3", "\u00c2", "\u00e2", "\u00f0", "\u00ef")


def _windows_mojibake_bytes(text: str) -> bytes:
    """Encode CP-1252 text while preserving its five undefined byte slots."""
    result = bytearray()
    for character in text:
        codepoint = ord(character)
        if codepoint in {0x81, 0x8D, 0x8F, 0x90, 0x9D}:
            result.append(codepoint)
        else:
            result.extend(character.encode("cp1252"))
    return bytes(result)


def repair_text_encoding(text: str) -> str:
    """Repair common UTF-8-as-Latin-1 corruption found in PDF text."""
    repaired = text or ""
    for _ in range(2):
        if not any(marker in repaired for marker in _MOJIBAKE_MARKERS):
            break
        try:
            candidate = _windows_mojibake_bytes(repaired).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
        if candidate == repaired:
            break
        repaired = candidate

    # Some PDFs use a private-use font glyph in place of a bullet point.
    return repaired.replace("\uf0d8", "\u2022")


def clean_text(text: str) -> str:
    """Clean extracted text while retaining paragraphs and list structure."""
    text = repair_text_encoding(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    text = re.sub(r"-\n(?=\w)", "", text)
    text = re.sub(r"(?<![.!?:\n])\n(?!\n)", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n ", "\n", text)
    return text.strip()
