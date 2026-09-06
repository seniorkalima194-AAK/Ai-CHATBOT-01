from unittest.mock import MagicMock, patch
import ollama
import pytest

from app.core.config import settings
from app.llm import gemma_client
from app.llm import ollama_client


def test_config_has_llm_settings():
    assert settings.ollama_model
    assert 0.0 <= settings.ollama_temperature <= 2.0
    assert settings.ollama_timeout > 0


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

@patch("app.llm.gemma_client.ollama_generate")
def test_gemma_generate_uses_stop_token(mock_generate):
    mock_generate.return_value = "Hello there!"

    gemma_client.generate(
        "You are a helpful assistant.",
        "Say hello.",
    )

    mock_generate.assert_called_once()

    _, kwargs = mock_generate.call_args

    assert kwargs["stop"] == ["<end_of_turn>"]


@patch("app.llm.gemma_client.ollama_generate")
def test_gemma_generate_builds_system_and_user_prompt(mock_generate):
    mock_generate.return_value = "Hello"

    gemma_client.generate(
        "You are a helpful assistant.",
        "Say hello.",
    )

    prompt = mock_generate.call_args.args[0]

    assert "<start_of_turn>system" in prompt
    assert "You are a helpful assistant." in prompt
    assert "<start_of_turn>user" in prompt
    assert "Say hello." in prompt
    assert "<start_of_turn>model" in prompt
