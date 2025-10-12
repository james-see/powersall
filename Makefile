# Makefile for powersall development

.PHONY: help install test lint format clean build publish bump-version

help: ## Show this help message
	@echo 'Available commands:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	uv pip install -e .

install-dev: ## Install with development dependencies
	uv pip install -e ".[dev]"

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=powersall --cov-report=html

lint: ## Run linting
	uv run black --check powersall/
	uv run isort --check-only powersall/
	uv run flake8 powersall/
	uv run mypy powersall/

format: ## Format code
	uv run black powersall/
	uv run isort powersall/

build: ## Build the package
	uv build

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

bump-version-patch: ## Bump patch version (e.g., 2.0.0 -> 2.0.1)
	uv run bump-version patch

bump-version-minor: ## Bump minor version (e.g., 2.0.0 -> 2.1.0)
	uv run bump-version minor

bump-version-major: ## Bump major version (e.g., 2.0.0 -> 3.0.0)
	uv run bump-version major

publish: ## Publish to PyPI (requires tag and PYPI_API_TOKEN secret)
	@echo "Publishing to PyPI..."
	@echo "Make sure you have:"
	@echo "1. Committed all changes"
	@echo "2. Created a git tag (e.g., git tag v2.0.0)"
	@echo "3. Set PYPI_API_TOKEN secret in GitHub repository"
	@echo "4. Pushed the tag (git push --tags)"

serve-docs: ## Serve documentation locally
	@echo "Starting documentation server..."
	cd docs && uv run astro dev

check-all: ## Run all checks (test, lint, format)
	$(MAKE) test
	$(MAKE) lint
	$(MAKE) format
