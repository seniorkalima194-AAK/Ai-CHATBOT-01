# Request/response schemas for chat interactions.
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """Request body sent by the client."""

    question: str = Field(
        ...,
        min_length=1,
        description="The student's question.",
        examples=["What is biology?"],
    )
    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Optional number of textbook chunks to retrieve. "
                     "Falls back to the server default when not set.",
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only questions (e.g. '   ')."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Question must not be empty or whitespace only.")
        return stripped


class ChatResponse(BaseModel):
    """Response returned by the chatbot API."""

    answer: str = Field(..., description="The generated answer.")
    answer_mode: Literal["pdf_grounded", "general_knowledge"]
    source_chunks: list[dict[str, Any]] = Field(default_factory=list)
