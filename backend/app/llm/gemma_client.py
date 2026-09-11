"""Model-agnostic chat wrapper for the configured Ollama model."""
from __future__ import annotations

import re

from app.documents.cleaner import repair_text_encoding
from app.llm.ollama_client import chat as ollama_chat


_CONTROL_TOKENS = re.compile(
    r"</?(?:think|s>|start_of_turn|end_of_turn|bos|eos)[^>]*>",
    flags=re.IGNORECASE,
)
_THINKING_BLOCK = re.compile(r"<think>.*?</think>", flags=re.IGNORECASE | re.DOTALL)


def _clean_response(text: str) -> str:
    """Remove accidental control tokens while preserving readable paragraphs."""
    cleaned = _THINKING_BLOCK.sub("", text or "")
    cleaned = _CONTROL_TOKENS.sub("", cleaned)
    lines = cleaned.splitlines()
    if lines and lines[0].strip().lower() in {"assistant", "model"}:
        cleaned = "\n".join(lines[1:])
    else:
        cleaned = re.sub(
            r"^\s*(?:assistant|model)\s*:\s*", "", cleaned, flags=re.I
        )
    return repair_text_encoding(cleaned).strip()


def generate(system_prompt: str, user_prompt: str) -> str:
    """Return a clean student-facing answer using Ollama's native chat format."""
    response = ollama_chat(
        [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ]
    )
    cleaned = _clean_response(response)
    if not cleaned:
        return "Sorry, I couldn't generate a readable answer. Please try again."
    return cleaned
