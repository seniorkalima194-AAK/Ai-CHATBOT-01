# Orchestration service for chat request handling.
import logging
from typing import Optional

from app.llm.ollama_client import OllamaError
from app.services.generation_service import generate_answer
from app.services.retrieval_service import retrieve_context

logger = logging.getLogger(__name__)


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