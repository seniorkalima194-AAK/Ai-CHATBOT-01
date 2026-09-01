# Tests for the answer generation service.
from unittest.mock import patch

from app.services.generation_service import SYSTEM_PROMPT, generate_answer


@patch("app.services.generation_service.generate")
def test_generate_answer_calls_gemma_with_system_and_user_prompt(mock_generate):
    """generate_answer() should pass the fixed SYSTEM_PROMPT and the given
    prompt through to the Gemma client, and return its result unchanged."""
    mock_generate.return_value = "The mitochondria is the powerhouse of the cell."

    result = generate_answer("Explain the mitochondria using this context: ...")

    assert result == "The mitochondria is the powerhouse of the cell."
    mock_generate.assert_called_once_with(
        system_prompt=SYSTEM_PROMPT,
        user_prompt="Explain the mitochondria using this context: ...",
    )


@patch("app.services.generation_service.generate")
def test_generate_answer_propagates_llm_errors(mock_generate):
    """generate_answer() should not swallow errors raised by the LLM client
    (that's chatbot_service's job) — they should propagate up unchanged."""
    from app.llm.ollama_client import OllamaTimeoutError

    mock_generate.side_effect = OllamaTimeoutError("Ollama request timed out")

    try:
        generate_answer("some prompt")
        assert False, "Expected OllamaTimeoutError to be raised"
    except OllamaTimeoutError:
        pass


@patch("app.services.generation_service.generate")
def test_generate_answer_system_prompt_mentions_context_rules(mock_generate):
    """Sanity check that the system prompt still instructs the model to
    rely on provided context and avoid inventing facts."""
    mock_generate.return_value = "answer"

    generate_answer("prompt")

    sent_system_prompt = mock_generate.call_args.kwargs["system_prompt"]
    assert "context" in sent_system_prompt.lower()
    assert "do not invent facts" in sent_system_prompt.lower()