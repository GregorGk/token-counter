# Token Counter Script for Gemini 3.0, Claude Opus 4.5, and ChatGPT 5.2

This repository now includes a specialized script (`count_tokens_for_file.py`) that counts tokens specifically for three advanced language models:
- **Gemini 3.0** (Google)
- **Claude Opus 4.5** (Anthropic)
- **ChatGPT 5.2** (OpenAI)

## Quick Start

```bash
# Count tokens for a single file
python count_tokens_for_file.py your_file.txt

# Output as JSON
python count_tokens_for_file.py your_file.txt --json

# Output as CSV
python count_tokens_for_file.py your_file.txt --csv
```

## Installation

First, ensure you have the token-counter package installed:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Script Features

The `count_tokens_for_file.py` script provides:

1. **Token Counting**: Counts tokens for all three models from a single text file
2. **Cost Estimation**: Estimates both input and output costs for each model
3. **Usage Analysis**: Shows percentage of context window used
4. **File Statistics**: Displays character, word, and line counts
5. **Comparison**: Shows which model is most efficient and cost-effective

## Example Output

```
╭─────────────────────────── File Statistics ────────────────────────────╮
│ File: sample.txt                                                        │
│ Size: 1,672 bytes                                                       │
│ Characters: 1,672                                                       │
│ Words: 256                                                              │
│ Lines: 5                                                                │
│ Avg word length: 5.42 chars                                             │
╰─────────────────────────────────────────────────────────────────────────╯

                        Token Count Analysis
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┓
┃ Model              ┃  Tokens ┃ Max Tokens ┃ Usage ┃ Input Cost┃ Output Cost┃ Total Cost┃ Status ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━┩
│ gemini-3.0         │     236 │  1,048,576 │  0.0% │  $0.001652│   $0.004956│  $0.006608│   ✓ OK │
│ claude-opus-4.5    │     427 │    500,000 │  0.1% │  $0.005124│   $0.021350│  $0.026474│   ✓ OK │
│ chatgpt-5.2        │     384 │    256,000 │  0.2% │  $0.007680│   $0.023040│  $0.030720│   ✓ OK │
└────────────────────┴─────────┴────────────┴───────┴───────────┴────────────┴───────────┴────────┘

Summary:
• Most efficient tokenization: gemini-3.0 (236 tokens)
• Least efficient tokenization: claude-opus-4.5 (427 tokens)
• Most cost-effective: gemini-3.0 ($0.006608)
• Token efficiency ratio: 1.81x difference between models
```

## Model Specifications

### Gemini 3.0
- **Max Tokens**: 1,048,576 (1M context window)
- **Input Cost**: $0.007 per 1K tokens
- **Output Cost**: $0.021 per 1K tokens
- **Tokenization**: Optimized for efficiency

### Claude Opus 4.5
- **Max Tokens**: 500,000
- **Input Cost**: $0.012 per 1K tokens
- **Output Cost**: $0.05 per 1K tokens
- **Tokenization**: Balanced for accuracy

### ChatGPT 5.2
- **Max Tokens**: 256,000
- **Input Cost**: $0.02 per 1K tokens
- **Output Cost**: $0.06 per 1K tokens
- **Tokenization**: Uses cl100k_base encoding

## Batch Processing

For processing multiple files, use the batch processor:

```bash
# Process multiple files
python examples/batch_token_counter.py *.txt

# Process specific files
python examples/batch_token_counter.py file1.txt file2.txt file3.txt
```

## Token Counting Methods

The script uses different tokenization approaches for each model:

1. **OpenAI (ChatGPT 5.2)**: Uses the official `tiktoken` library with cl100k_base encoding
2. **Anthropic (Claude Opus 4.5)**: Uses an approximation algorithm based on word and character counts
3. **Google (Gemini 3.0)**: Uses an optimized approximation that reflects Gemini's efficient tokenization

## Output Formats

### Standard (Table)
Default rich terminal output with colored tables and summaries.

### JSON
```json
{
  "file": "sample.txt",
  "text_statistics": {
    "characters": 1672,
    "words": 256,
    "lines": 5,
    "avg_word_length": 5.42
  },
  "models": {
    "gemini-3.0": {
      "tokens": 236,
      "input_cost": 0.001652,
      ...
    }
  }
}
```

### CSV
```csv
Model,Tokens,MaxTokens,Usage%,InputCost,OutputCost,TotalCost,ExceedsLimit
gemini-3.0,236,1048576,0.02,0.001652,0.004956,0.006608,False
...
```

## Notes

- Token counts are approximations for Anthropic and Google models
- Actual API token counts may vary slightly
- Cost estimates assume a 1:1 input/output ratio (adjustable in code)
- The script handles UTF-8 encoded text files

## Extending the Script

To add more models:

1. Update `token_counter/models.py` with new model configurations
2. Add tokenization logic in `token_counter/counter.py` if needed
3. Update `TARGET_MODELS` in the script to include new models