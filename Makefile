.PHONY: install dev lint typecheck test test-all bench clean

install:  ## Install in production mode
	pip install .

dev:  ## Install in editable mode with dev + bench extras
	pip install -e ".[dev,bench]"

lint:  ## Run linter (ruff)
	ruff check src/ tests/ benchmarks/
	ruff format --check src/ tests/ benchmarks/

format:  ## Auto-format code
	ruff format src/ tests/ benchmarks/
	ruff check --fix src/ tests/ benchmarks/

typecheck:  ## Run type checker (mypy)
	mypy src/epsleuth/

test:  ## Run unit tests (skip slow)
	pytest -m "not slow and not benchmark" -q

test-all:  ## Run all tests including slow
	pytest -q

bench:  ## Run benchmarks
	pytest benchmarks/ -m benchmark --benchmark-enable --benchmark-sort=fullname

check: lint typecheck test  ## Run all checks (lint + typecheck + test)

clean:  ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info src/*.egg-info .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
