# Tests for the retrieval service.
from unittest.mock import Mock, patch

from app.services.retrieval_service import retrieve_context


@patch("app.services.retrieval_service.get_pipeline")
def test_retrieve_context_calls_pipeline_run(mock_get_pipeline):
    """retrieve_context() should get the shared pipeline and call .run()
    with the question and top_k, returning its RAGResult unchanged."""
    mock_pipeline = Mock()
    mock_result = Mock()
    mock_pipeline.run.return_value = mock_result
    mock_get_pipeline.return_value = mock_pipeline

    result = retrieve_context("What is biology?", top_k=5)

    assert result is mock_result
    mock_pipeline.run.assert_called_once_with("What is biology?", top_k=5)


@patch("app.services.retrieval_service.get_pipeline")
def test_retrieve_context_defaults_top_k_to_none(mock_get_pipeline):
    """When top_k isn't given, retrieve_context() should pass None through
    and let the pipeline apply its own default."""
    mock_pipeline = Mock()
    mock_get_pipeline.return_value = mock_pipeline

    retrieve_context("What is biology?")

    mock_pipeline.run.assert_called_once_with("What is biology?", top_k=None)


@patch("app.services.retrieval_service.get_pipeline")
def test_retrieve_context_reuses_cached_pipeline(mock_get_pipeline):
    """retrieve_context() should call get_pipeline() (which is cached via
    lru_cache) rather than constructing a new RAGPipeline itself."""
    mock_pipeline = Mock()
    mock_get_pipeline.return_value = mock_pipeline

    retrieve_context("question one")
    retrieve_context("question two")

    assert mock_get_pipeline.call_count == 2  # cheap call, lru_cache handles reuse
    assert mock_pipeline.run.call_count == 2


@patch("app.services.retrieval_service.get_pipeline")
def test_retrieve_context_propagates_pipeline_errors(mock_get_pipeline):
    """A ValueError raised by the pipeline (e.g. empty question) should
    propagate up unchanged — chatbot_service is responsible for handling it."""
    mock_pipeline = Mock()
    mock_pipeline.run.side_effect = ValueError("Question must not be empty.")
    mock_get_pipeline.return_value = mock_pipeline

    try:
        retrieve_context("")
        assert False, "Expected ValueError to be raised"
    except ValueError as exc:
        assert str(exc) == "Question must not be empty."