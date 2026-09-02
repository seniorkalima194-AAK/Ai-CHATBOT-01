# Service responsible for retrieving relevant learning material.
from typing import Optional

from app.rag.pipeline import RAGResult, get_pipeline


def retrieve_context(
    question: str,
    top_k: Optional[int] = None,
) -> RAGResult:
    """
    Retrieve relevant learning material for a student question.

    The RAG pipeline handles the actual retrieval work.
    This service only provides a simple interface for the chatbot service.
    """
    pipeline = get_pipeline()

    result = pipeline.run(
        question,
        top_k=top_k,
    )

    return result