# Placeholder: client wrapper for the Ollama LLM integration.
from typing import Any

import ollama

from app.core.config import settings


class OllamaError(Exception):
    """Base exception for Ollama client errors."""


class OllamaConnectionError(OllamaError):
    """Raised when Ollama cannot be reached."""


class OllamaTimeoutError(OllamaError):
    """Raised when an Ollama request times out."""


class OllamaModelNotFoundError(OllamaError):
    """Raised when the configured model is not pulled."""


def _get_client() -> ollama.Client:
    """Create an Ollama client using application configuration."""
    return ollama.Client(
        host=settings.ollama_host,
        timeout=settings.ollama_timeout,
    )


def health_check() -> bool:
    """
    Check whether Ollama is reachable and the configured model is pulled.

    Returns:
        True when Ollama is reachable and the configured model exists.

    Raises:
        OllamaConnectionError:
            If Ollama cannot be reached.
        OllamaModelNotFoundError:
            If the configured model is not pulled.
    """
    client = _get_client()

    try:
        response = client.list()
    except Exception as exc:
        raise OllamaConnectionError(
            "Ollama unreachable"
        ) from exc

    configured_model = settings.ollama_model

    models = getattr(response, "models", [])

    model_names = {
        getattr(model, "model", None)
        for model in models
    }

    if configured_model not in model_names:
        raise OllamaModelNotFoundError(
            f"Model not pulled: {configured_model}"
        )

    return True


def generate(
        prompt: str,
        stop:list[str] | None=None,
        ) -> str:
    """
    Send a prompt to the configured Ollama model.

    Args:
        prompt: Prompt to send to the model.

    Returns:
        Raw generated text.

    Raises:
        OllamaConnectionError:
            If Ollama cannot be reached or the request fails.
        OllamaTimeoutError:
            If the request times out.
        OllamaModelNotFoundError:
            If the configured model is not pulled.
    """
    client = _get_client()

    try:
        response: Any = client.generate(
            model=settings.ollama_model,
            prompt=prompt,
            options={
                "temperature": settings.ollama_temperature,
                "stop": stop or [],
            },
        )

        return response.response

    except ollama.ResponseError as exc:
        if getattr(exc, "status_code", None) == 404:
            raise OllamaModelNotFoundError(
                f"Model not pulled: {settings.ollama_model}"
            ) from exc

        raise OllamaConnectionError(
            f"Ollama request failed: {exc}"
        ) from exc

    except TimeoutError as exc:
        raise OllamaTimeoutError(
            "Ollama request timed out"
        ) from exc

    except Exception as exc:
        raise OllamaConnectionError(
            f"Ollama request failed: {exc}"
        ) from exc
