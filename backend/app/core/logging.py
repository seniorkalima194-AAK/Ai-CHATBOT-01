# Placeholder: centralized logging configuration.


from __future__ import annotations

import logging
import sys

import structlog

from app.core.config import settings

_LOG_LEVEL_BY_ENV = {
    "development": logging.DEBUG,
    "production": logging.INFO,
}

_configured = False


def configure_logging() -> None:
    """
    Configure structlog + stdlib logging exactly once per process.
    Safe to call more than once — later calls are no-ops, so importing
    this module from several places never installs duplicate handlers.
    """
    global _configured
    if _configured:
        return

    log_level = _LOG_LEVEL_BY_ENV.get(settings.environment, logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
        force=True,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.CallsiteParameterAdder(
                [structlog.processors.CallsiteParameter.MODULE]
            ),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    _configured = True


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a configured logger. Pass __name__ for an explicit module label."""
    configure_logging()
    return structlog.get_logger(name)


def bind_request_context(**kwargs) -> None:
    """Attach fields (e.g. request_id) to every log line until cleared."""
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_request_context() -> None:
    structlog.contextvars.clear_contextvars()


configure_logging()
logger = get_logger()