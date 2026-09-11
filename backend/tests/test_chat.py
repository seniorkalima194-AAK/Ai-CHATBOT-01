# Tests for the chatbot orchestration service.
from unittest.mock import Mock, patch

import pytest

from app.llm.ollama_client import OllamaConnectionError
from app.services.chatbot_service import chat


@patch("app.services.chatbot_service.generate_answer")
@patch("app.services.chatbot_service.retrieve_context")
def test_chat_returns_answer_for_valid_question(mock_retrieve, mock_generate):
    """chat() should retrieve context, generate an answer, and return it."""
    mock_result = Mock(prompt="built prompt with context")
    mock_retrieve.return_value = mock_result
    mock_generate.return_value = "Photosynthesis is how plants make food."

    answer = chat("What is photosynthesis?")

    assert answer == "Photosynthesis is how plants make food."
    mock_retrieve.assert_called_once_with("What is photosynthesis?", top_k=None)
    mock_generate.assert_called_once_with("built prompt with context")


@patch("app.services.chatbot_service.generate_answer")
@patch("app.services.chatbot_service.retrieve_context")
def test_chat_forwards_top_k(mock_retrieve, mock_generate):
    """chat() should forward a custom top_k to retrieve_context."""
    mock_retrieve.return_value = Mock(prompt="prompt")
    mock_generate.return_value = "answer"

    chat("What is biology?", top_k=6)

    mock_retrieve.assert_called_once_with("What is biology?", top_k=6)


@pytest.mark.parametrize("question", ["", "   ", "\n\t"])
def test_chat_rejects_empty_or_blank_question(question):
    """chat() should short-circuit on empty/whitespace input without
    calling retrieval or generation at all."""
    with patch("app.services.chatbot_service.retrieve_context") as mock_retrieve:
        answer = chat(question)

        assert answer == "Please ask a question."
        mock_retrieve.assert_not_called()


@patch("app.services.chatbot_service.retrieve_context")
def test_chat_handles_ollama_error_gracefully(mock_retrieve):
    """chat() should catch OllamaError (and subclasses) and return a
    friendly message instead of raising."""
    mock_retrieve.side_effect = OllamaConnectionError("Ollama unreachable")

    answer = chat("What is gravity?")

    assert "couldn't generate an answer" in answer.lower()


@patch("app.services.chatbot_service.retrieve_context")
def test_chat_handles_value_error_from_pipeline(mock_retrieve):
    """chat() should surface a ValueError raised deeper in the pipeline
    (e.g. from RAGPipeline.run) as its message, without crashing."""
    mock_retrieve.side_effect = ValueError("Question must not be empty.")

    answer = chat("some question")

    assert answer == "Question must not be empty."