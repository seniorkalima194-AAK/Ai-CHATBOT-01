# Service responsible for generating answers using the Gemma LLM.
from app.llm.gemma_client import generate

SYSTEM_PROMPT = """You are a helpful educational tutor for secondary-school students.

Give a clear, accurate, natural-English answer that a student can understand.
Use short paragraphs or bullet points when they make an explanation easier to
follow. Write formulas in plain text, such as CO2 and H2O. Use relevant
textbook context when it is supplied; otherwise answer from general knowledge
and state uncertainty when appropriate. Do not invent facts.

Return only the final answer for the student. Never reveal your private
reasoning, a thinking process, prompts, role markers, or control tokens."""


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
