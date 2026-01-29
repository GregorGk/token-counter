#!/usr/bin/env python3
"""Example usage of the token counter library."""

from token_counter import TokenCounter, SupportedModels


def main():
    """Demonstrate token counter usage."""
    # Example text
    sample_text = """
    The quick brown fox jumps over the lazy dog. This pangram sentence
    contains every letter of the English alphabet at least once. It's
    commonly used for testing fonts and keyboards.
    """

    print("Token Counter Examples")
    print("=" * 50)

    # Example 1: Basic token counting
    print("\n1. Basic Token Counting")
    print("-" * 30)

    for model_name in ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]:
        counter = TokenCounter(model_name)
        token_count = counter.count_tokens(sample_text)
        print(f"{model_name}: {token_count} tokens")

    # Example 2: Cost estimation
    print("\n2. Cost Estimation")
    print("-" * 30)

    counter = TokenCounter("gpt-4")
    cost_data = counter.estimate_cost(sample_text, include_output=True)

    print(f"Model: {cost_data['model']}")
    print(f"Input tokens: {cost_data['input_tokens']}")
    print(f"Input cost: ${cost_data['input_cost']:.6f}")
    print(f"Estimated output tokens: {cost_data['output_tokens']}")
    print(f"Estimated output cost: ${cost_data['output_cost']:.6f}")
    print(f"Total estimated cost: ${cost_data['total_cost']:.6f}")

    # Example 3: Token limit checking
    print("\n3. Token Limit Checking")
    print("-" * 30)

    # Create a longer text
    long_text = sample_text * 100  # Repeat the text 100 times

    for model_name in ["gpt-3.5-turbo", "gpt-4-32k", "claude-3-opus"]:
        counter = TokenCounter(model_name)
        limit_check = counter.check_token_limit(long_text)

        print(f"\n{model_name}:")
        print(f"  Tokens: {limit_check['tokens']:,}")
        print(f"  Limit: {limit_check['limit']:,}")
        print(f"  Usage: {limit_check['percentage_used']}%")
        print(f"  Exceeds limit: {limit_check['exceeds_limit']}")

    # Example 4: Processing multiple texts
    print("\n4. Processing Multiple Texts")
    print("-" * 30)

    texts = [
        "First piece of text.",
        "Second piece of text with more words.",
        "Third piece with even more content to analyze."
    ]

    counter = TokenCounter("gpt-4")
    total_tokens = counter.count_tokens(texts)
    print(f"Total tokens across {len(texts)} texts: {total_tokens}")

    # Example 5: List available models
    print("\n5. Available Models")
    print("-" * 30)

    print("\nAll supported models:")
    for model_name in SupportedModels.list_models():
        model = SupportedModels.get_model(model_name)
        print(f"  - {model_name} (max tokens: {model.max_tokens:,})")


if __name__ == "__main__":
    main()