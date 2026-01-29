# Token Counter

A comprehensive command-line tool for counting tokens in text for various Large Language Model (LLM) providers. Updated with the latest 2026 models and pricing.

## Features

- Count tokens for OpenAI models (GPT-5, GPT-4, GPT-3.5, etc.)
- Count tokens for Anthropic Claude models (Opus 4.5, Sonnet 4.5, Haiku 4.5)
- Count tokens for Google Gemini models (Gemini 3 Pro, Flash)
- Count tokens for Mistral AI models (Medium 3, Small 3.1, OCR)
- Count tokens for Cohere models (Command, Command-R, Command-Light)
- Estimate API costs based on token usage with 2026 pricing
- Support for multiple encoding methods
- Read from files or stdin
- Batch processing of multiple files
- Check token limits for models
- JSON, CSV, and table output formats

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
# Count tokens for text
token-counter -t 'Hello, world!' -m gpt-5

# Count tokens for Claude Opus 4.5
token-counter -t 'Hello, world!' -m claude-opus-4.5

# Count tokens from a file
token-counter -f input.txt -m gemini-3-flash

# Count tokens from multiple files
token-counter -F file1.txt -F file2.txt -m gpt-4o-mini

# Count tokens from stdin
echo 'Hello, world!' | token-counter -m gpt-5

# Get cost estimate with expected output tokens
token-counter -t "Your text here" -m gpt-5 -c -o 1000

# Check if text exceeds model token limit
token-counter -f large_document.txt -m claude-sonnet-4.5 -l

# List all supported models
token-counter --list-models

# Output in different formats
token-counter -t "Hello" -m gpt-5 --format json
token-counter -t "Hello" -m gpt-5 --format table
```

## Supported Models (2026 Latest)

### OpenAI Models
| Model | Context Window | Input Cost/1M | Output Cost/1M | Notes |
|-------|---------------|---------------|----------------|-------|
| **gpt-5** | 400K | $1.25 | $10.00 | Latest flagship model |
| **gpt-5-codex** | 400K | $1.25 | $10.00 | Optimized for code |
| **gpt-5.2** | 400K | $1.25 | $10.00 | Enhanced version |
| **gpt-4.1** | 1M | $2.00 | $8.00 | Largest context window |
| **gpt-4o** | 128K | $2.50 | $10.00 | Optimized variant |
| **gpt-4o-mini** | 128K | $0.15 | $0.60 | Cost-effective option |
| gpt-4 | 8K | $30.00 | $60.00 | Legacy |
| gpt-4-turbo | 128K | $10.00 | $30.00 | Legacy |
| gpt-3.5-turbo | 4K | $0.50 | $1.50 | Legacy |
| **gpt-oss-20b** | 128K | $0.02 | $0.02 | Most affordable |

### Anthropic Claude Models
| Model | Context Window | Input Cost/1M | Output Cost/1M | Notes |
|-------|---------------|---------------|----------------|-------|
| **claude-opus-4.5** | 200K | $5.00 | $25.00 | Most capable, 67% cheaper than 4.1 |
| **claude-sonnet-4.5** | 200K | $3.00 | $15.00 | Balanced performance |
| **claude-sonnet-4.5-long** | 1M | $6.00 | $22.50 | Extended context |
| **claude-haiku-4.5** | 200K | $1.00 | $5.00 | Fast & affordable |
| claude-3-opus | 200K | $15.00 | $75.00 | Legacy |
| claude-3-sonnet | 200K | $3.00 | $15.00 | Legacy |
| claude-3-haiku | 200K | $0.25 | $1.25 | Legacy |

### Google Gemini Models
| Model | Context Window | Input Cost/1M | Output Cost/1M | Notes |
|-------|---------------|---------------|----------------|-------|
| **gemini-3-pro** | 200K | $2.00 | $12.00 | Preview pricing |
| **gemini-3-pro-long** | 1M | $4.00 | $18.00 | Long context |
| **gemini-3-flash** | 1M | $0.50 | $3.00 | 3x faster than 2.5 Pro |
| gemini-3.0 | 1M | $7.00 | $21.00 | Legacy |

### Mistral AI Models
| Model | Context Window | Input Cost/1M | Output Cost/1M | Notes |
|-------|---------------|---------------|----------------|-------|
| **mistral-medium-3** | 128K | $0.40 | $0.40 | Beats Llama 4 & Cohere |
| **mistral-small-3.1** | 128K | $0.20 | $0.20 | Multimodal capable |
| **mistral-ocr** | 128K | $0.40 | $0.40 | OCR specialized |

### Cohere Models
| Model | Context Window | Input Cost/1K | Output Cost/1K | Notes |
|-------|---------------|---------------|----------------|-------|
| **command** | 4K | $1.50 | $2.00 | Enterprise-focused |
| **command-r** | 128K | $1.50 | $2.00 | RAG optimized |
| **command-light** | 4K | $0.30 | $0.60 | Budget option |

**Note**: Prices are in USD. Some providers offer discounts for batch processing or caching.

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

## Model Updates (January 2026)

This tool includes the latest models and pricing as of January 29, 2026:

- **OpenAI**: Added GPT-5 series (including GPT-5.2 and GPT-5 Codex) with significantly reduced pricing
- **Anthropic**: Updated to Claude 4.5 series with 67% cost reduction compared to Claude 4.1
- **Google**: Added Gemini 3 Pro and Flash models currently in preview
- **Mistral**: Added Medium 3, Small 3.1, and OCR models
- **Cohere**: Added Command series with RAG-optimized variants

## Changelog

### v0.3.0 (January 29, 2026)
- Added support for latest 2026 models:
  - OpenAI GPT-5, GPT-5.2, GPT-5 Codex, GPT-4.1, GPT-4o series
  - Anthropic Claude 4.5 series (Opus, Sonnet, Haiku)
  - Google Gemini 3 series (Pro, Flash)
  - Mistral AI models (Medium 3, Small 3.1, OCR)
  - Cohere models (Command, Command-R, Command-Light)
- Updated pricing to reflect 2026 rates
- Added support for extended context windows (up to 1M tokens)
- Improved documentation with comprehensive model comparison

### v0.2.0
- Added security documentation and offline verification
- Fixed JSON and CSV output formatting
- Initial support for Gemini 3.0, Claude Opus 4.5, and ChatGPT 5.2

### v0.1.0
- Initial release
- Basic token counting functionality
- Support for OpenAI and Anthropic models

## License

MIT