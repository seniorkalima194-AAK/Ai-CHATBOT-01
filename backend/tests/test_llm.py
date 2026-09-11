from unittest.mock import MagicMock, patch
import ollama
import pytest

from app.core.config import settings
from app.llm import gemma_client
from app.llm import ollama_client


def test_config_has_llm_settings():
    assert settings.ollama_model == "gemma4:latest"
    assert settings.ollama_temperature == 0.2
    assert settings.ollama_timeout == 120.0


@patch("app.llm.ollama_client._get_client")
def test_health_check_success(mock_get_client):
    mock_client = MagicMock()
    mock_client.list.return_value = MagicMock(
        models=[
            MagicMock(model=settings.ollama_model),
        ]
    )

    mock_get_client.return_value = mock_client

    assert ollama_client.health_check() is True


@patch("app.llm.ollama_client._get_client")
def test_health_check_model_not_pulled(mock_get_client):
    mock_client = MagicMock()
    mock_client.list.return_value = MagicMock(
        models=[
            MagicMock(model="different-model"),
        ]
    )

    mock_get_client.return_value = mock_client

    with pytest.raises(ollama_client.OllamaModelNotFoundError):
        ollama_client.health_check()


@patch("app.llm.ollama_client._get_client")
def test_health_check_ollama_unreachable(mock_get_client):
    mock_client = MagicMock()
    mock_client.list.side_effect = ConnectionError("connection refused")

    mock_get_client.return_value = mock_client

    with pytest.raises(ollama_client.OllamaConnectionError):
        ollama_client.health_check()


@patch("app.llm.ollama_client._get_client")
def test_generate_returns_raw_text(mock_get_client):
    mock_client = MagicMock()
    mock_client.generate.return_value = MagicMock(
        response="Hello from Gemma"
    )

    mock_get_client.return_value = mock_client

    result = ollama_client.generate("Say hello")

    assert result == "Hello from Gemma"


@patch("app.llm.ollama_client._get_client")
def test_generate_model_not_found(mock_get_client):
    mock_client = MagicMock()

    error = ollama.ResponseError(
        "model not found",
        status_code=404,
    )

    mock_client.generate.side_effect = error
    mock_get_client.return_value = mock_client

    with pytest.raises(ollama_client.OllamaModelNotFoundError):
        ollama_client.generate("Hello")


@patch("app.llm.ollama_client._get_client")
def test_generate_timeout(mock_get_client):
    mock_client = MagicMock()
    mock_client.generate.side_effect = TimeoutError()

    mock_get_client.return_value = mock_client

    with pytest.raises(ollama_client.OllamaTimeoutError):
        ollama_client.generate("Hello")

@patch("app.llm.gemma_client.ollama_chat")
def test_gemma_generate_uses_native_ollama_chat_and_cleans_tokens(mock_chat):
    mock_chat.return_value = "<think>private reasoning</think><start_of_turn>model\nHello there!<end_of_turn>"

    answer = gemma_client.generate(
        "You are a helpful assistant.",
        "Say hello.",
    )

    assert answer == "Hello there!"
    mock_chat.assert_called_once_with(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello."},
        ]
    )


@patch("app.llm.ollama_client._get_client")
def test_chat_uses_ollama_role_messages(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.return_value = MagicMock(message=MagicMock(content="Clear answer"))
    mock_get_client.return_value = mock_client

    answer = ollama_client.chat([
        {"role": "system", "content": "Be clear."},
        {"role": "user", "content": "What is biology?"},
    ])

    assert answer == "Clear answer"
    assert mock_client.chat.call_args.kwargs["messages"] == [
        {"role": "system", "content": "Be clear."},
        {"role": "user", "content": "What is biology?"},
    ]
    assert mock_client.chat.call_args.kwargs["think"] is False
