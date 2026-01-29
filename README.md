# Token Counter

A command-line tool for counting tokens in text for various Large Language Model (LLM) providers.

## Features

- Count tokens for OpenAI models (GPT-3.5, GPT-4, etc.)
- Count tokens for Anthropic Claude models
- Estimate API costs based on token usage
- Support for multiple encoding methods
- Read from files or stdin
- Batch processing of multiple files

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd token-counter

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

```bash
# Count tokens for OpenAI GPT-4
token-counter "Hello, world!" --model gpt-4

# Count tokens for Claude
token-counter "Hello, world!" --model claude-3-opus

# Count tokens from a file
token-counter --file input.txt --model gpt-3.5-turbo

# Count tokens from stdin
echo "Hello, world!" | token-counter --model gpt-4

# Get cost estimate
token-counter "Your text here" --model gpt-4 --estimate-cost
```

## Supported Models

### OpenAI
- gpt-4
- gpt-4-32k
- gpt-3.5-turbo
- text-davinci-003
- And more...

### Anthropic
- claude-3-opus
- claude-3-sonnet
- claude-3-haiku
- claude-2.1
- claude-2.0

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black token_counter

# Type checking
mypy token_counter
```

## License

MIT