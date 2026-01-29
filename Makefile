.PHONY: help install install-dev test lint format clean build

help:
	@echo "Available commands:"
	@echo "  make install      Install the package"
	@echo "  make install-dev  Install with development dependencies"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linters (flake8, mypy)"
	@echo "  make format      Format code with black"
	@echo "  make clean       Clean build artifacts"
	@echo "  make build       Build distribution packages"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	flake8 token_counter tests
	mypy token_counter

format:
	black token_counter tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel