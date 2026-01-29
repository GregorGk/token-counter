"""Model configurations and supported models."""

from dataclasses import dataclass
from typing import Dict, Optional, Literal
from enum import Enum


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


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
    "gpt-4": ModelConfig(
        name="gpt-4",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=8192,
        input_cost_per_1k=0.03,
        output_cost_per_1k=0.06
    ),
    "gpt-4-32k": ModelConfig(
        name="gpt-4-32k",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=32768,
        input_cost_per_1k=0.06,
        output_cost_per_1k=0.12
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
    "gpt-3.5-turbo-16k": ModelConfig(
        name="gpt-3.5-turbo-16k",
        provider=Provider.OPENAI,
        encoding="cl100k_base",
        max_tokens=16384,
        input_cost_per_1k=0.003,
        output_cost_per_1k=0.004
    ),
}

# Anthropic model configurations
ANTHROPIC_MODELS: Dict[str, ModelConfig] = {
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
    "claude-2.1": ModelConfig(
        name="claude-2.1",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=200000,
        input_cost_per_1k=0.008,
        output_cost_per_1k=0.024
    ),
    "claude-2.0": ModelConfig(
        name="claude-2.0",
        provider=Provider.ANTHROPIC,
        encoding="claude",
        max_tokens=100000,
        input_cost_per_1k=0.008,
        output_cost_per_1k=0.024
    ),
}

# All supported models
SUPPORTED_MODELS: Dict[str, ModelConfig] = {
    **OPENAI_MODELS,
    **ANTHROPIC_MODELS
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