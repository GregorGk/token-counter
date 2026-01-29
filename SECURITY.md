# Security & Privacy Information

## Data Privacy

**All token counting is performed locally on your machine. No text data is ever sent to external servers.**

### How It Works

1. **OpenAI Models (GPT-4, ChatGPT 5.2, etc.)**
   - Uses the `tiktoken` library for offline tokenization
   - Encoding rules are downloaded once and cached locally
   - All tokenization happens on your machine
   - No API calls are made to count tokens

2. **Anthropic Models (Claude models)**
   - Uses a local approximation algorithm
   - Based on word and character counting
   - No network connections required
   - No API authentication needed

3. **Google Models (Gemini)**
   - Uses a local approximation algorithm
   - Pure mathematical calculations
   - Completely offline operation

### What Data Stays Local

- ✅ Your text files
- ✅ Token counts
- ✅ Cost calculations
- ✅ All processing

### What Goes Online

- ⬇️ One-time download of tiktoken encoding files (cached for future use)
- ❌ None of your actual text content

### Verification

You can verify this by:

1. **Checking network activity**: Run the tool while monitoring network traffic - you'll see no outbound data
2. **Reviewing the source code**: All tokenization logic is in `token_counter/counter.py`
3. **Running offline**: Disconnect from internet after initial setup - the tool still works

### For Maximum Security

```bash
# 1. Install the package
pip install -e .

# 2. Run once to download tiktoken encodings
token-counter --list-models

# 3. Disconnect from internet
# 4. Use freely with confidential data
python count_tokens_for_file.py confidential.txt
```

### Limitations

- Token counts for Anthropic and Google models are approximations
- For exact token counts, you would need to use their APIs (which would send data online)
- The approximations are reasonably accurate for cost estimation purposes

## Dependencies Security

- `tiktoken`: Official OpenAI library, well-maintained and secure
- `rich`: Terminal formatting only, no network features used
- `click`: Command-line interface library, no network features used
- `anthropic`: Installed but not used for actual API calls

## License

This tool is open source under MIT license. You can review, audit, and modify the code as needed.