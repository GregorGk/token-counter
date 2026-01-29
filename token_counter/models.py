"""Model configurations and supported models."""

from dataclasses import dataclass
from typing import Dict, Optional, Literal
from enum import Enum


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    COHERE = "cohere"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""

    name: str
    provider: Provider
    encoding: str
    max_tokens: int
    input_cost_per_1k: float  # Cost per 1000 tokens
    output_cost_per_1k: Optional[float] = None  # Some models have different output costs

    @property
    def cost_per_token(self) -> float:
        """Get cost per single input token."""
        return self.input_cost_per_1k / 1000


# OpenAI model configurations
OPENAI_MODELS: Dict[str, ModelConfig] = {
    # GPT-5 Series (Latest 2026)
    "gpt-5": ModelConfig(
        name="gpt-5",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=400000,
        input_cost_per_1k=0.00125,  # $1.25 per 1M tokens
        output_cost_per_1k=0.01     # $10.00 per 1M tokens
    ),
    "gpt-5-codex": ModelConfig(
        name="gpt-5-codex",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=400000,
        input_cost_per_1k=0.00125,  # $1.25 per 1M tokens
        output_cost_per_1k=0.01     # $10.00 per 1M tokens
    ),
    "gpt-5.2": ModelConfig(
        name="gpt-5.2",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=400000,
        input_cost_per_1k=0.00125,  # $1.25 per 1M tokens
        output_cost_per_1k=0.01     # $10.00 per 1M tokens
    ),
    # GPT-4 Series
    "gpt-4.1": ModelConfig(
        name="gpt-4.1",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=1000000,  # 1M context window
        input_cost_per_1k=0.002,    # $2.00 per 1M tokens
        output_cost_per_1k=0.008    # $8.00 per 1M tokens
    ),
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.0025,   # $2.50 per 1M tokens
        output_cost_per_1k=0.01     # $10.00 per 1M tokens
    ),
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.00015,  # $0.150 per 1M tokens
        output_cost_per_1k=0.0006   # $0.600 per 1M tokens
    ),
    # Legacy models (still available)
    "gpt-4": ModelConfig(
        name="gpt-4",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=8192,
        input_cost_per_1k=0.03,
        output_cost_per_1k=0.06
    ),
    "gpt-4-turbo": ModelConfig(
        name="gpt-4-turbo",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.01,
        output_cost_per_1k=0.03
    ),
    "gpt-3.5-turbo": ModelConfig(
        name="gpt-3.5-turbo",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=4096,
        input_cost_per_1k=0.0005,
        output_cost_per_1k=0.0015
    ),
    # Most affordable option
    "gpt-oss-20b": ModelConfig(
        name="gpt-oss-20b",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.00002,  # $0.02 per 1M tokens
        output_cost_per_1k=0.00002
    ),
}

# Anthropic model configurations
ANTHROPIC_MODELS: Dict[str, ModelConfig] = {
    # Claude 4.5 Series (Latest 2026)
    "claude-opus-4.5": ModelConfig(
        name="claude-opus-4.5",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.005,    # $5 per 1M tokens
        output_cost_per_1k=0.025    # $25 per 1M tokens
    ),
    "claude-sonnet-4.5": ModelConfig(
        name="claude-sonnet-4.5",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.003,    # $3 per 1M tokens
        output_cost_per_1k=0.015    # $15 per 1M tokens
    ),
    "claude-sonnet-4.5-long": ModelConfig(
        name="claude-sonnet-4.5-long",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=1000000,  # 1M context
        input_cost_per_1k=0.006,    # $6 per 1M tokens (>200K context)
        output_cost_per_1k=0.0225   # $22.50 per 1M tokens
    ),
    "claude-haiku-4.5": ModelConfig(
        name="claude-haiku-4.5",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.001,    # $1 per 1M tokens
        output_cost_per_1k=0.005    # $5 per 1M tokens
    ),
    # Legacy Claude 3 models (still available)
    "claude-3-opus": ModelConfig(
        name="claude-3-opus",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.015,
        output_cost_per_1k=0.075
    ),
    "claude-3-sonnet": ModelConfig(
        name="claude-3-sonnet",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.003,
        output_cost_per_1k=0.015
    ),
    "claude-3-haiku": ModelConfig(
        name="claude-3-haiku",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.00025,
        output_cost_per_1k=0.00125
    ),
}

# Google model configurations
GOOGLE_MODELS: Dict[str, ModelConfig] = {
    # Gemini 3 Series (Latest 2026)
    "gemini-3-pro": ModelConfig(
        name="gemini-3-pro",
        provider=Provider.GOOGLE,
        encoding="gemini",
        max_tokens=200000,  # Standard context
        input_cost_per_1k=0.002,    # $2.00 per 1M tokens
        output_cost_per_1k=0.012    # $12.00 per 1M tokens
    ),
    "gemini-3-pro-long": ModelConfig(
        name="gemini-3-pro-long",
        provider=Provider.GOOGLE,
        encoding="gemini",
        max_tokens=1000000,  # 1M context window
        input_cost_per_1k=0.004,    # $4.00 per 1M tokens (>200K)
        output_cost_per_1k=0.018    # $18.00 per 1M tokens
    ),
    "gemini-3-flash": ModelConfig(
        name="gemini-3-flash",
        provider=Provider.GOOGLE,
        encoding="gemini",
        max_tokens=1000000,
        input_cost_per_1k=0.0005,   # $0.50 per 1M tokens
        output_cost_per_1k=0.003    # $3.00 per 1M tokens
    ),
    # Legacy Gemini models
    "gemini-3.0": ModelConfig(
        name="gemini-3.0",
        provider=Provider.GOOGLE,
        encoding="gemini",
        max_tokens=1048576,  # 1M context window
        input_cost_per_1k=0.007,
        output_cost_per_1k=0.021
    ),
}

# Mistral model configurations
MISTRAL_MODELS: Dict[str, ModelConfig] = {
    "mistral-medium-3": ModelConfig(
        name="mistral-medium-3",
        provider=Provider.MISTRAL,
        encoding="cl100k_base",  # Mistral uses similar tokenization
        max_tokens=128000,
        input_cost_per_1k=0.0004,   # $0.40 per 1M tokens
        output_cost_per_1k=0.0004
    ),
    "mistral-small-3.1": ModelConfig(
        name="mistral-small-3.1",
        provider=Provider.MISTRAL,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.0002,   # Estimated based on being cheaper than medium
        output_cost_per_1k=0.0002
    ),
    "mistral-ocr": ModelConfig(
        name="mistral-ocr",
        provider=Provider.MISTRAL,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.0004,
        output_cost_per_1k=0.0004
    ),
}

# Cohere model configurations
COHERE_MODELS: Dict[str, ModelConfig] = {
    "command": ModelConfig(
        name="command",
        provider=Provider.COHERE,
        encoding="cl100k_base",  # Cohere uses similar tokenization
        max_tokens=4000,
        input_cost_per_1k=0.0015,   # $1.50 per 1K tokens
        output_cost_per_1k=0.002    # $2.00 per 1K tokens
    ),
    "command-r": ModelConfig(
        name="command-r",
        provider=Provider.COHERE,
        encoding="cl100k_base",
        max_tokens=128000,
        input_cost_per_1k=0.0015,
        output_cost_per_1k=0.002
    ),
    "command-light": ModelConfig(
        name="command-light",
        provider=Provider.COHERE,
        encoding="cl100k_base",
        max_tokens=4000,
        input_cost_per_1k=0.0003,   # $0.30 per 1K tokens
        output_cost_per_1k=0.0006   # $0.60 per 1K tokens
    ),
}

# All supported models
SUPPORTED_MODELS: Dict[str, ModelConfig] = {
    **OPENAI_MODELS,
    **ANTHROPIC_MODELS,
    **GOOGLE_MODELS,
    **MISTRAL_MODELS,
    **COHERE_MODELS
}


class SupportedModels:
    """Helper class for model operations."""

    @staticmethod
    def get_all() -> Dict[str, ModelConfig]:
        """Get all supported models."""
        return SUPPORTED_MODELS

    @staticmethod
    def get_model(name: str) -> Optional[ModelConfig]:
        """Get a specific model by name."""
        return SUPPORTED_MODELS.get(name)

    @staticmethod
    def get_provider_models(provider: Provider) -> Dict[str, ModelConfig]:
        """Get all models for a specific provider."""
        return {
            name: config
            for name, config in SUPPORTED_MODELS.items()
            if config.provider == provider
        }

    @staticmethod
    def list_models() -> list[str]:
        """Get a list of all model names."""
        return list(SUPPORTED_MODELS.keys())