# Placeholder: client wrapper for the Gemma LLM integration.
from app.llm.ollama_client import generate as ollama_generate


_SPECIAL_TOKENS = (
    "<start_of_turn>",
    "<end_of_turn>",
    "<start_of_turn>system",
    "<start_of_turn>user",
    "<start_of_turn>model",
    "<eos>",
    "<bos>",
)


def _build_prompt(system_prompt: str, user_prompt: str) -> str:
    """Build a Gemma chat prompt using system and user roles."""
    return (
        f"<start_of_turn>system\n"
        f"{system_prompt.strip()}"
        f"<end_of_turn>\n"
        f"<start_of_turn>user\n"
        f"{user_prompt.strip()}"
        f"<end_of_turn>\n"
        f"<start_of_turn>model\n"
    )

def _clean_response(text: str) -> str:
    """Remove leftover Gemma role markers and special tokens."""
    cleaned = text

    # Remove complete role markers first.
    role_markers = (
        "<start_of_turn>system",
        "<start_of_turn>user",
        "<start_of_turn>model",
        "<end_of_turn>",
    )

    for marker in role_markers:
        cleaned = cleaned.replace(marker, "")

    # Remove remaining special tokens.
    special_tokens = (
        "<start_of_turn>",
        "<eos>",
        "<bos>",
    )

    for token in special_tokens:
        cleaned = cleaned.replace(token, "")

    # Remove leftover role labels.
    lines = cleaned.splitlines()

    if lines and lines[0].strip().lower() in {
        "system",
        "user",
        "model",
        "assistant",
    }:
        lines = lines[1:]

    return "\n".join(lines).strip()


def generate(system_prompt: str, user_prompt: str) -> str:
    """
    Generate a clean response from the configured Gemma model.

    Args:
        system_prompt: Instructions describing the assistant's behavior.
        user_prompt: User's actual request.

    Returns:
        Clean plain-text model response.
    """
    prompt = _build_prompt(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    response = ollama_generate(
        prompt,
        stop=["<end_of_turn>"],
        )

    return _clean_response(response)