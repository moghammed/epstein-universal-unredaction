# Contributing to epstein-universal-unredaction

Thanks for your interest in contributing! This guide will help you get started.

## Development Setup

```bash
git clone https://github.com/epstein-universal-unredaction/epstein-universal-unredaction.git
cd epstein-universal-unredaction
pip install -e ".[dev,bench]"
```

## How the Pipeline Works

epstein-universal-unredaction uses a **Fat Payload** architecture. A single `Payload` object (defined in `src/epstein_universal_unredaction/payload.py`) flows through 7 sequential steps. Each step:

1. Reads data written by earlier steps.
2. Writes its own results under well-known keys.
3. Never deletes or overwrites keys owned by earlier steps.

The orchestrator (`src/epstein_universal_unredaction/pipeline.py`) handles routing and per-step timing.

## Working on a Step

Each step lives in `src/epstein_universal_unredaction/steps/step{N}_{name}.py` and exposes a single function:

```python
def run(payload: Payload) -> Payload:
    ...
```

The stub files contain detailed docstrings explaining what each step should do, what it reads, and what it writes. Start there.

### Conventions

- **Coordinates**: all bounding boxes are normalized to `[0, 1]`. Use helpers in `src/epstein_universal_unredaction/utils/coords.py`.
- **Physical units**: all physical measurements (page size, gap width, character width) are in **millimeters**.
- **IDs**: use the pattern `p{page}_b{block}` for blocks, `p{page}_r{index}` for redactions.

## Running Checks

```bash
make check       # lint + typecheck + test (all three)
make test        # unit tests only (fast)
make test-all    # all tests including slow/integration
make bench       # benchmarks
make format      # auto-format code
```

## Code Style

- Enforced by `ruff` (config in `pyproject.toml`).
- Type annotations required; checked by `mypy --strict`.
- Run `make format` before committing.

## Tests

- **Unit tests** go in `tests/unit/`. One file per source module.
- **Integration tests** go in `tests/integration/`. Mark slow tests with `@pytest.mark.slow`.
- **Fixtures** (test PDFs) go in `tests/fixtures/`.
- Shared fixtures are defined in `tests/conftest.py`.

When implementing a step, add corresponding tests that:
1. Test the step in isolation with a synthetic payload.
2. Test edge cases (empty pages, no redactions, etc.).
3. Validate that the step writes the correct keys without corrupting earlier data.

## Benchmarks

Benchmark scaffolding is in `benchmarks/bench_pipeline.py`. When you implement a step, add a benchmark that exercises it with a realistic synthetic payload.

## Pull Request Checklist

- [ ] `make check` passes (lint + typecheck + tests)
- [ ] New code has type annotations
- [ ] Step stubs updated or replaced with implementations
- [ ] Tests added for new functionality
- [ ] Docstrings updated if the public API changed
