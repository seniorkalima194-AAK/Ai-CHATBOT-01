from app.rag.prompt_builder import build_prompt
from app.rag.retriever import RetrievedChunk


def test_build_prompt_uses_textbook_context_when_the_match_is_relevant():
    chunk = RetrievedChunk(
        text="Biology is the study of living things.",
        source="biology.pdf",
        score=0.9,
        metadata={"page": 1},
    )

    prompt = build_prompt("What is biology?", [chunk], pdf_grounded=True)

    assert "TEXTBOOK EXCERPTS" in prompt
    assert "Biology is the study of living things." in prompt
    assert "What is biology?" in prompt


def test_build_prompt_uses_general_knowledge_when_no_match_is_relevant():
    prompt = build_prompt("What is the capital of France?", [], pdf_grounded=False)

    assert "Answer from general knowledge" in prompt
    assert "What is the capital of France?" in prompt
