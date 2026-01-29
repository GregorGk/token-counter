"""Core token counting functionality."""

import tiktoken
from anthropic import Anthropic
from typing import Optional, Union, List
from .models import ModelConfig, Provider, SupportedModels


class TokenCounter:
    """Main class for counting tokens across different LLM providers."""

    def __init__(self, model: str):
        """Initialize token counter for a specific model.

        Args:
            model: Model name (e.g., 'gpt-4', 'claude-3-opus')

        Raises:
            ValueError: If model is not supported
        """
        self.model_config = SupportedModels.get_model(model)
        if not self.model_config:
            supported = ", ".join(SupportedModels.list_models())
            raise ValueError(f"Model '{model}' not supported. Supported models: {supported}")

        self._encoder = None
        self._anthropic_client = None

    def count_tokens(self, text: Union[str, List[str]]) -> int:
        """Count tokens in text.

        Args:
            text: Single string or list of strings to count tokens for

        Returns:
            Total number of tokens
        """
        if isinstance(text, list):
            return sum(self.count_tokens(t) for t in text)

        if self.model_config.provider == Provider.OPENAI:
            return self._count_openai_tokens(text)
        elif self.model_config.provider == Provider.ANTHROPIC:
            return self._count_anthropic_tokens(text)
        else:
            raise ValueError(f"Unknown provider: {self.model_config.provider}")

    def _count_openai_tokens(self, text: str) -> int:
        """Count tokens using OpenAI's tiktoken library."""
        if self._encoder is None:
            try:
                self._encoder = tiktoken.encoding_for_model(self.model_config.name)
            except KeyError:
                # Fall back to the encoding name if model not found
                self._encoder = tiktoken.get_encoding(self.model_config.encoding)

        return len(self._encoder.encode(text))

    def _count_anthropic_tokens(self, text: str) -> int:
        """Count tokens for Anthropic models."""
        if self._anthropic_client is None:
            # Initialize without API key for token counting
            self._anthropic_client = Anthropic(api_key="dummy")

        # Use Anthropic's token counting method
        # Note: This is a simplified version. In practice, Anthropic's
        # token counting is more complex and depends on the specific model
        # For now, we'll use a rough approximation
        return self._approximate_anthropic_tokens(text)

    def _approximate_anthropic_tokens(self, text: str) -> int:
        """Approximate token count for Anthropic models.

        This is a simplified approximation. For production use,
        you should use Anthropic's official token counting API.
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        # This is not accurate but provides a reasonable estimate
        words = text.split()
        chars = len(text)

        # Use a weighted average of word count and character count
        # This gives a better approximation than just characters
        estimated_tokens = int((len(words) * 1.3) + (chars / 4)) // 2

        return estimated_tokens

    def estimate_cost(self, text: Union[str, List[str]],
                     include_output: bool = False,
                     output_tokens: Optional[int] = None) -> dict:
        """Estimate the cost of processing text.

        Args:
            text: Text to process
            include_output: Whether to include output cost estimation
            output_tokens: Number of output tokens (if known)

        Returns:
            Dictionary with token counts and cost estimates
        """
        input_tokens = self.count_tokens(text)
        input_cost = (input_tokens / 1000) * self.model_config.input_cost_per_1k

        result = {
            "model": self.model_config.name,
            "input_tokens": input_tokens,
            "input_cost": round(input_cost, 6),
            "max_tokens": self.model_config.max_tokens,
            "tokens_remaining": self.model_config.max_tokens - input_tokens
        }

        if include_output and self.model_config.output_cost_per_1k:
            if output_tokens is None:
                # Estimate output tokens as 50% of input tokens
                output_tokens = int(input_tokens * 0.5)

            output_cost = (output_tokens / 1000) * self.model_config.output_cost_per_1k
            result.update({
                "output_tokens": output_tokens,
                "output_cost": round(output_cost, 6),
                "total_tokens": input_tokens + output_tokens,
                "total_cost": round(input_cost + output_cost, 6)
            })

        return result

    def check_token_limit(self, text: Union[str, List[str]]) -> dict:
        """Check if text exceeds model's token limit.

        Args:
            text: Text to check

        Returns:
            Dictionary with validation results
        """
        token_count = self.count_tokens(text)
        exceeds_limit = token_count > self.model_config.max_tokens

        return {
            "tokens": token_count,
            "limit": self.model_config.max_tokens,
            "exceeds_limit": exceeds_limit,
            "percentage_used": round((token_count / self.model_config.max_tokens) * 100, 2)
        }