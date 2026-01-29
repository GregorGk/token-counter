# Supported Models and Pricing (January 2026)

This document provides detailed information about all supported models, their capabilities, and current pricing as of January 29, 2026.

## OpenAI Models

### Latest GPT-5 Series
- **GPT-5** ([Released August 7, 2025](https://pricepertoken.com/pricing-page/model/openai-gpt-5))
  - Context: 400K tokens
  - Pricing: $1.25 input / $10.00 output per 1M tokens
  - Most affordable flagship model

- **GPT-5 Codex** ([Released September 23, 2025](https://pricepertoken.com/pricing-page/model/openai-gpt-5-codex))
  - Context: 400K tokens
  - Pricing: $1.25 input / $10.00 output per 1M tokens
  - Optimized for code generation and understanding

- **GPT-5.2** ([Latest version](https://platform.openai.com/docs/models/gpt-5.2))
  - Context: 400K tokens
  - Pricing: $1.25 input / $10.00 output per 1M tokens
  - Enhanced capabilities over base GPT-5

### GPT-4 Variants
- **GPT-4.1** ([Released April 14, 2025](https://pricepertoken.com/pricing-page/model/openai-gpt-4.1))
  - Context: 1M tokens (largest available)
  - Pricing: $2.00 input / $8.00 output per 1M tokens

- **GPT-4o** ([Optimized variant](https://pricepertoken.com/pricing-page/model/openai-gpt-4o))
  - Context: 128K tokens
  - Pricing: $2.50 input / $10.00 output per 1M tokens

- **GPT-4o-mini** ([Budget option](https://pricepertoken.com/pricing-page/model/openai-gpt-4o-mini))
  - Context: 128K tokens
  - Pricing: $0.15 input / $0.60 output per 1M tokens

### Most Affordable
- **GPT-OSS-20b**
  - Context: 128K tokens
  - Pricing: $0.02 per 1M tokens (both input/output)
  - Currently the most affordable option

## Anthropic Claude Models

### Claude 4.5 Series ([Released November 24, 2025](https://www.anthropic.com/news/claude-opus-4-5))

- **Claude Opus 4.5**
  - Context: 200K tokens
  - Pricing: $5 input / $25 output per 1M tokens
  - 67% cheaper than Opus 4.1 while delivering superior performance
  - Achieves 80.9% on SWE-bench Verified

- **Claude Sonnet 4.5**
  - Context: 200K tokens (standard), 1M tokens (extended)
  - Standard pricing: $3 input / $15 output per 1M tokens
  - Long context pricing (>200K): $6 input / $22.50 output per 1M tokens
  - Designed for agentic workflows

- **Claude Haiku 4.5**
  - Context: 200K tokens
  - Pricing: $1 input / $5 output per 1M tokens
  - Near-frontier performance at 5x lower cost than Sonnet
  - Ideal for real-time chat and high-volume tasks

### Special Features
- **Batch Processing**: 50% discount on both input and output tokens
- **Prompt Caching**: Can reduce costs by up to 90%
- **Extended Thinking**: Available on all 4.5 models, billed as output tokens

## Google Gemini Models

### Gemini 3 Series ([Launched late 2025](https://blog.google/products/gemini/gemini-3-flash/))

- **Gemini 3 Pro** (Preview)
  - Standard context (≤200K): $2.00 input / $12.00 output per 1M tokens
  - Long context (>200K): $4.00 input / $18.00 output per 1M tokens
  - Features Deep Think functionality for complex reasoning
  - Expected stable pricing: $1.50/$10 (≤200K) and $3/$15 (>200K)

- **Gemini 3 Flash**
  - Context: 1M tokens
  - Pricing: $0.50 input / $3.00 output per 1M tokens
  - 3x faster than Gemini 2.5 Pro at a fraction of the cost
  - Audio input: $1.00 per 1M tokens

### Technical Details
- Processing over 1T tokens per day on API
- Native multimodal understanding (text, images, audio, video, code)
- Grounding with Google Search begins January 5, 2026

## Mistral AI Models

### Latest Models ([2026 releases](https://mistral.ai/news/mistral-medium-3))

- **Mistral Medium 3**
  - Context: 128K tokens
  - Pricing: $0.40 per 1M tokens (both input/output)
  - Surpasses Llama 4 Maverick and Cohere Command A

- **Mistral Small 3.1**
  - Context: 128K tokens
  - Pricing: $0.20 per 1M tokens (estimated)
  - Features multimodal capabilities

- **Mistral OCR**
  - Context: 128K tokens
  - Pricing: $0.40 per 1M tokens
  - Specialized for optical character recognition

## Cohere Models

### Command Series ([Enterprise-focused](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration))

- **Command**
  - Context: 4K tokens
  - Pricing: $1.50 input / $2.00 output per 1K tokens

- **Command-R**
  - Context: 128K tokens
  - Pricing: $1.50 input / $2.00 output per 1K tokens
  - RAG-optimized with native function calling

- **Command-Light**
  - Context: 4K tokens
  - Pricing: $0.30 input / $0.60 output per 1K tokens
  - Budget-friendly option

### Additional Services
- **Rerank Service**: $2.00 per 1,000 searches
- **Embed Models**: $0.10 per 1M tokens
- **Provisioned Throughput**: $39.60/hour for consistent high-volume usage

## Token Calculation Notes

- **Text**: ~4 characters or 0.75 words = 1 token (English)
- **Images**: Fixed 560 tokens regardless of size (Gemini)
- **Video**: 258 tokens per second at 1 FPS (Gemini)
- **Audio**: 25 tokens per second without timestamps (Gemini)

## Sources

- [OpenAI Pricing](https://platform.openai.com/docs/pricing)
- [Anthropic Claude API Docs](https://platform.claude.com/docs/en/about-claude/pricing)
- [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Mistral AI News](https://mistral.ai/news/mistral-medium-3)
- [Cohere Pricing](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- [Comprehensive API Pricing Comparison](https://pricepertoken.com)

*Last updated: January 29, 2026*