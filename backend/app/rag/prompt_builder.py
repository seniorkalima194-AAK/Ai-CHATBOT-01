# Placeholder: prompt assembly for grounded LLM responses.

from __future__ import annotations

from typing import List

from app.rag.retriever import RetrievedChunk
#inaelezea jukumu la AI kwa shule za Tanzania
SYSTEM_INSTRUCTION = (
    "You are a helpful educational tutor for Tanzanian secondary school students "
    "(TIE syllabus).\n"
    "Answer the student's question using ONLY the information provided in the "
    "CONTEXT below.\n"
    "If the context does not contain enough information to answer the question, "
    'reply with exactly:\n'
    '"I don\'t know based on the available learning materials."\n'
    "Do not invent facts, do not use external knowledge, and do not speculate.\n"
    "Keep your answer clear, concise, and suitable for a student."
)

#hii inaunganisha chunks za RAG na swali la mwanafunzi kuwa prompt moja
def build_prompt(
    question: str,
    chunks: List[RetrievedChunk],
    max_context_chars: int = 3500,
) -> str:
    """
    Combine retrieved chunks and the student question into a Gemma-ready prompt.

    Explicitly instructs the model to stay inside the supplied context and to
    say "I don't know..." when the context is insufficient.
    """
    if not chunks:
        context_block = "(No relevant learning material was found.)"
    else:
        parts: List[str] = []
        total = 0
        for i, chunk in enumerate(chunks, start=1):
            piece = f"[Source {i}: {chunk.source}]\n{chunk.text.strip()}"
            if total + len(piece) > max_context_chars:
                break
            parts.append(piece)
            total += len(piece) + 2
        context_block = "\n\n".join(parts)
#hii ndio sehemu inayo kamilisha hii function
        prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"CONTEXT:\n{context_block}\n\n"
        f"STUDENT QUESTION:\n{question.strip()}\n\n"
        f"ANSWER:"
    )
    return prompt


def estimate_prompt_tokens(prompt: str) -> int:
    """Rough token estimate (~4 characters per token for English)."""
    return max(1, len(prompt) // 4)