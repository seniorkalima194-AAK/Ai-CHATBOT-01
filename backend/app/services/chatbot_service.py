# Orchestration service for chat request handling.
import logging
from dataclasses import dataclass
from typing import Any, Optional

from app.llm.ollama_client import OllamaError
from app.services.generation_service import generate_answer
from app.services.retrieval_service import retrieve_context

logger = logging.getLogger(__name__)


@dataclass
class ChatResult:
    answer: str
    answer_mode: str
    source_chunks: list[dict[str, Any]]


def chat(question: str, top_k: Optional[int] = None) -> str:
    """
    Handle a complete chat request.

    The service:
    1. Retrieves relevant context for the question (from the ingested
       PDF textbooks, via the RAG pipeline).
    2. Sends that context to the generation service.
    3. Returns the generated answer.

    Never raises for expected failure modes (empty question, LLM
    unreachable) — returns a friendly message instead, so the caller
    (e.g. a FastAPI endpoint) can return it directly.
    """
    if not question or not question.strip():
        return "Please ask a question."

    try:
        result = retrieve_context(question, top_k=top_k)
        return generate_answer(result.prompt)

    except OllamaError:
        logger.exception("LLM generation failed for question: %s", question)
        return (
            "Sorry, I couldn't generate an answer right now. "
            "Please make sure the AI model (Ollama) is running and try again."
        )

    except ValueError as exc:
        return str(exc)


def chat_with_metadata(question: str, top_k: Optional[int] = None) -> ChatResult:
    """Generate an answer plus transparent mode and PDF source information."""
    if not question or not question.strip():
        return ChatResult("Please ask a question.", "general_knowledge", [])
    try:
        result = retrieve_context(question, top_k=top_k)
        answer = generate_answer(result.prompt)
        sources = []
        if result.answer_mode == "pdf_grounded":
            sources = [
                {"source": chunk.source, "page": chunk.metadata.get("page"), "score": chunk.score}
                for chunk in result.chunks
            ]
        return ChatResult(answer, result.answer_mode, sources)
    except OllamaError:
        logger.exception("LLM generation failed for question: %s", question)
        return ChatResult("Sorry, I couldn't generate an answer right now. Please make sure Ollama is running and try again.", "general_knowledge", [])
    except (ValueError, RuntimeError) as exc:
        return ChatResult(str(exc), "general_knowledge", [])
