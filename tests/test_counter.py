"""Tests for token counter functionality."""

import pytest
from token_counter import TokenCounter, SupportedModels


def test_token_counter_initialization():
    """Test TokenCounter initialization with valid model."""
    counter = TokenCounter("gpt-4")
    assert counter.model_config.name == "gpt-4"


def test_invalid_model():
    """Test TokenCounter with invalid model."""
    with pytest.raises(ValueError) as exc_info:
        TokenCounter("invalid-model")
    assert "not supported" in str(exc_info.value)


def test_openai_token_counting():
    """Test token counting for OpenAI models."""
    counter = TokenCounter("gpt-4")

    # Test simple text
    text = "Hello, world!"
    tokens = counter.count_tokens(text)
    assert tokens > 0
    assert tokens < 10  # Simple text should have few tokens


def test_token_counting_list():
    """Test token counting with list of texts."""
    counter = TokenCounter("gpt-4")
    texts = ["Hello", "world", "from", "Python"]
    tokens = counter.count_tokens(texts)
    assert tokens > 0


def test_cost_estimation():
    """Test cost estimation functionality."""
    counter = TokenCounter("gpt-4")
    text = "This is a test text for cost estimation."

    result = counter.estimate_cost(text)
    assert "input_tokens" in result
    assert "input_cost" in result
    assert result["input_cost"] > 0


def test_cost_estimation_with_output():
    """Test cost estimation with output tokens."""
    counter = TokenCounter("gpt-4")
    text = "Test input"

    result = counter.estimate_cost(text, include_output=True, output_tokens=100)
    assert "output_tokens" in result
    assert result["output_tokens"] == 100
    assert "total_cost" in result


def test_token_limit_check():
    """Test token limit checking."""
    counter = TokenCounter("gpt-3.5-turbo")
    text = "Short text"

    result = counter.check_token_limit(text)
    assert "tokens" in result
    assert "limit" in result
    assert "exceeds_limit" in result
    assert result["exceeds_limit"] is False
    assert result["percentage_used"] < 1.0


def test_supported_models():
    """Test SupportedModels helper class."""
    all_models = SupportedModels.get_all()
    assert len(all_models) > 0

    model_list = SupportedModels.list_models()
    assert "gpt-4" in model_list
    assert "claude-3-opus" in model_list

    gpt4 = SupportedModels.get_model("gpt-4")
    assert gpt4 is not None
    assert gpt4.name == "gpt-4"