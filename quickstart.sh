#!/bin/bash
# Quick start script for token-counter

echo "Token Counter - Quick Start"
echo "=========================="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install package in development mode
echo "Installing token-counter..."
pip install -e ".[dev]"

echo
echo "✓ Setup complete!"
echo
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Try the CLI: token-counter --help"
echo "  3. Count tokens: token-counter -t 'Hello, world!' -m gpt-4"
echo "  4. List models: token-counter --list-models"
echo
echo "For more examples, see the README.md file."