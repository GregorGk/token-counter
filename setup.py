from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="token-counter",
    version="0.3.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for counting tokens for various LLM providers (2026 models)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "tiktoken>=0.5.0",  # For OpenAI token counting
        "anthropic>=0.7.0",  # For Anthropic token counting
        "click>=8.0.0",  # For CLI interface
        "rich>=13.0.0",  # For nice terminal output
        "pyyaml>=6.0",  # For config files
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=1.0.0",
            "flake8>=5.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "token-counter=token_counter.cli:main",
            "count-tokens-for-file=count_tokens_for_file:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)