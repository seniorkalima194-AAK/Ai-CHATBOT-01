# Placeholder: end-to-end RAG pipeline orchestration.
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.core.config import settings
from app.core.logging import logger
from app.rag.prompt_builder import build_prompt, estimate_prompt_tokens
from app.rag.retriever import RetrievedChunk, Retriever

#hii inafafanya kazi kama record ya kila run moja ya mfumo
@dataclass
class RAGResult:
    """Result of one pipeline run."""

    question: str
    prompt: str
    chunks: List[RetrievedChunk]
    prompt_token_estimate: int
    answer_mode: str

#hii inaunganisha hatua zote za mfumo wa rag kwa pamoja kutoka swali la mwanafunzi hadi prompt ya mwisho
class RAGPipeline:
    """
    Orchestrates:
        question → embed → retrieve top-k → build grounded prompt

    Does NOT call Gemma. The finished prompt is handed to the generation service.
    """

    def __init__(
        self,
        retriever: Optional[Retriever] = None,
        top_k: Optional[int] = None,
    ) -> None:
        self.top_k = top_k if top_k is not None else settings.top_k
        self.retriever = retriever or Retriever(top_k=self.top_k)

    def run(self, question: str, top_k: Optional[int] = None) -> RAGResult:
        """
        Execute retrieval + prompt building for one student question.

        Returns a RAGResult that contains the ready-to-send prompt and the
        supporting chunks (useful for source citations later).
        """
        question = (question or "").strip()
        if not question:
            raise ValueError("Question cannot be empty.")

        k = top_k if top_k is not None else self.top_k
        chunks = self.retriever.retrieve(question, top_k=k)
        pdf_grounded = bool(
            chunks and chunks[0].score >= settings.similarity_threshold
        )
        prompt = build_prompt(question, chunks if pdf_grounded else [], pdf_grounded)
        token_est = estimate_prompt_tokens(prompt)

        logger.info(
            "rag_pipeline_complete",
            question_preview=question[:80],
            chunks_retrieved=len(chunks),
            prompt_chars=len(prompt),
            prompt_token_estimate=token_est,
            answer_mode="pdf_grounded" if pdf_grounded else "general_knowledge",
        )

        if token_est > 6000:
            logger.warning(
                "prompt_may_be_long",
                token_estimate=token_est,
                hint="Consider lowering TOP_K or CHUNK_SIZE",
            )

        return RAGResult(
            question=question,
            prompt=prompt,
            chunks=chunks,
            prompt_token_estimate=token_est,
            answer_mode="pdf_grounded" if pdf_grounded else "general_knowledge",
        )


# Lazy singleton
_default_pipeline: Optional[RAGPipeline] = None


def get_pipeline() -> RAGPipeline:
    global _default_pipeline
    if _default_pipeline is None:
        _default_pipeline = RAGPipeline()
    return _default_pipeline


def run(question: str, top_k: Optional[int] = None) -> RAGResult:
    """Convenience shortcut that uses the default pipeline."""
    return get_pipeline().run(question, top_k=top_k)

