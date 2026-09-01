# Placeholder: application configuration and environment settings.


from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from sentence_transformers import SentenceTransformer

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Single source of truth for backend environment variables.

    Other modules must import `settings` from here instead of reading
    environment variables directly.
    """

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="forbid",
        case_sensitive=False,
    )

    # LLM
    llm_model_name: str = Field(..., min_length=1)
    llm_temperature: float = Field(..., ge=0.0, le=2.0)
    llm_timeout_seconds: int = Field(default=60, gt=0)

    # RAG
    chunk_size: int = Field(..., gt=0)
    chunk_overlap: int = Field(..., ge=0)
    top_k: int = Field(..., gt=0)

        # Embeddings
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", min_length=1
    )

    # Vector database
    vector_db_path: Path = Field(...)



    # HTTP / CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )

    # Application environment
    environment: str = Field(default="development", min_length=1)

    @model_validator(mode="after")
    def validate_chunking(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


# This runs during startup and fails immediately for missing/invalid settings.
settings = get_settings()
