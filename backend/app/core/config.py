"""Central configuration for the offline educational chatbot."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"


class Settings(BaseSettings):
    """The one supported environment-variable contract for the backend."""

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="forbid",
        case_sensitive=False,
    )

    # Local LLM (Ollama)
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = Field(..., min_length=1)
    ollama_temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    ollama_timeout: float = Field(default=120.0, gt=0)

    # Retrieval-Augmented Generation
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", min_length=1
    )
    chunk_size: int = Field(default=400, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)
    top_k: int = Field(default=5, ge=1, le=20)
    similarity_threshold: float = Field(default=0.50, ge=-1.0, le=1.0)

    # Chroma data is deliberately not stored beside Python source files.
    raw_documents_path: Path = DATA_DIR / "raw" / "educational_materials"
    processed_documents_path: Path = DATA_DIR / "processed"
    vector_db_path: Path = DATA_DIR / "chroma"

    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )
    environment: str = Field(default="development", min_length=1)

    @model_validator(mode="after")
    def validate_chunking(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
