# Service responsible for generating answers using the Gemma LLM.
from app.llm.gemma_client import generate

SYSTEM_PROMPT = """You are an educational assistant.

Answer the student's question clearly and accurately.
Use the provided context when available.
If the context does not contain enough information, say so clearly.
Do not invent facts."""


def generate_answer(prompt: str) -> str:
    """
    Generate an answer using the configured Gemma model.

    Args:
        prompt: The prompt prepared by the RAG pipeline.

    Returns:
        The generated answer as plain text.

    Raises:
        OllamaError (and subclasses): propagated if the LLM is unreachable,
        times out, or is not pulled. Handled by the calling service.
    """
    return generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
    )