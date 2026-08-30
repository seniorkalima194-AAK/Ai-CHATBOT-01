# Placeholder: document chunking logic for vector embedding and retrieval.
import re

#jinsi document inavyogawanyika katika vipande
def _tokenize(text: str) -> list[str]:
    """
    split text into smaller chunks
    """
    return text.split()

#hii function inapokea na kurudisha string
#.!? tafuta alama ya mwisho ya sentensi
#=< sentensi itagawanyika baada ya kuona alama hizi
#\s+ baada ya kuona hizi alama mgawanyiko hutokea
#text.strip inaondoa nafasi tupu mwanzo au mwisho mwa sentensi

def _split_sentences(text: str) -> list[str]:
    """
    Split text approximately at sentence boundaries.
    """
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """
    Split text into chunks while trying to respect
    sentence boundaries.

    Args:
        text: Cleaned text.
        chunk_size: Maximum number of tokens.
        overlap: Number of tokens shared between chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    sentences = _split_sentences(text)

    chunks = []
    current_tokens = []

    for sentence in sentences:
        sentence_tokens = _tokenize(sentence)

        if not sentence_tokens:
            continue

        # If adding this sentence exceeds the limit,
        # finalize the current chunk.
        if (
            current_tokens
            and len(current_tokens) + len(sentence_tokens)
            > chunk_size
        ):
            chunks.append(" ".join(current_tokens))

            # Keep overlap tokens
            current_tokens = current_tokens[
                max(0, len(current_tokens) - overlap):
            ]

        # kwa sentensi ndefu zaidi
        if len(sentence_tokens) > chunk_size:
            start = 0

            while start < len(sentence_tokens):
                end = min(start + chunk_size, len(sentence_tokens))

                chunks.append(
                    " ".join(sentence_tokens[start:end])
                )

                start += chunk_size - overlap

            current_tokens = []
            continue

        current_tokens.extend(sentence_tokens)

    if current_tokens:
        chunks.append(" ".join(current_tokens))

    return chunks