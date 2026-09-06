# Placeholder: client wrapper for the Ollama LLM integration.
from typing import Any, Mapping, Sequence

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


def chat(messages: Sequence[Mapping[str, str]]) -> str:
    """Send role-based messages through Ollama's native chat API.

    Ollama applies the correct template for the configured model. This avoids
    nesting Gemma control tokens inside another model template, which was the
    source of malformed and hard-to-read responses.
    """
    client = _get_client()

    try:
        response: Any = client.chat(
            model=settings.ollama_model,
            messages=[dict(message) for message in messages],
            # Gemma 4 otherwise returns its private reasoning in a separate
            # field before generating the answer. Students need the answer,
            # not the model's internal working.
            think=False,
            options={"temperature": settings.ollama_temperature},
        )
        message = getattr(response, "message", None)
        if message is None and isinstance(response, Mapping):
            message = response.get("message")
        content = getattr(message, "content", None)
        if content is None and isinstance(message, Mapping):
            content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise OllamaConnectionError("Ollama returned an empty chat response")
        return content

    except ollama.ResponseError as exc:
        if getattr(exc, "status_code", None) == 404:
            raise OllamaModelNotFoundError(
                f"Model not pulled: {settings.ollama_model}"
            ) from exc
        raise OllamaConnectionError(f"Ollama request failed: {exc}") from exc
    except TimeoutError as exc:
        raise OllamaTimeoutError("Ollama request timed out") from exc
    except OllamaError:
        raise
    except Exception as exc:
        raise OllamaConnectionError(f"Ollama request failed: {exc}") from exc
