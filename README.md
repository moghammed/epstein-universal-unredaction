# epstein-universal-unredaction

Reverse-engineer black-box redactions in PDF documents using spatial and typographic analysis.

epstein-universal-unredaction is an open-source pipeline that examines the geometry of redaction boxes, the fonts and character metrics of surrounding text, and the semantic context of each gap to produce ranked guesses of what was redacted. It does **not** rely on basic OCR; instead it leans on precise typographic math.

## Architecture

The pipeline follows a **Fat Payload** design: a single `Payload` object (a Pydantic model) is initialized in Step 1 and passed sequentially through seven steps. Each step reads what it needs and writes its results under well-known keys. No step deletes or overwrites data owned by an earlier step.

**Coordinate convention:** all spatial coordinates are normalized to `[0, 1]`. Physical dimensions are in millimeters (mm).

### Pipeline Steps

| # | Step                  | Module                        | Writes to payload                              |
|---|----------------------|-------------------------------|-------------------------------------------------|
| 1 | Document Ingestion   | `steps/step1_ingest.py`       | `meta`, `pages`                                 |
| 2 | Logical Segmentation | `steps/step2_segment.py`      | `blocks_by_page`                                |
| 3 | Redaction ID & Context | `steps/step3_redactions.py` | `redactions_by_page`                            |
| 4 | Typographic Profiling | `steps/step4_typographic.py` | `typographic_profile`, `gaps_by_redaction_id`   |
| 5 | Semantic Classification | `steps/step5_classify.py`  | `predictions_by_redaction_id`                   |
| 6 | Dictionary Matching  | `steps/step6_candidates.py`   | `candidates_by_redaction_id`                    |
| 7 | Consolidation        | `steps/step7_consolidate.py`  | `output`                                        |

## Quick Start

```bash
# Clone and install in development mode
git clone https://github.com/epstein-universal-unredaction/epstein-universal-unredaction.git
cd epstein-universal-unredaction
pip install -e ".[dev,bench]"

# List pipeline steps
epstein-universal-unredaction steps

# Run on a PDF (will fail with NotImplementedError until steps are implemented)
epstein-universal-unredaction run document.pdf -o results.json -vv

# Run tests
pytest

# Run benchmarks
pytest benchmarks/ -m benchmark --benchmark-enable
```

## Project Structure

```
epstein-universal-unredaction/
├── src/epstein_universal_unredaction/
│   ├── __init__.py          # Package root, version
│   ├── cli.py               # CLI entry point (argparse)
│   ├── payload.py           # Fat Payload schema (Pydantic models)
│   ├── pipeline.py          # Orchestrator: step registry, routing, timing
│   ├── steps/
│   │   ├── step1_ingest.py       # Document Ingestion & Triage
│   │   ├── step2_segment.py      # Logical Segmentation
│   │   ├── step3_redactions.py   # Redaction ID & Context Extraction
│   │   ├── step4_typographic.py  # Typographic & Spatial Profiling
│   │   ├── step5_classify.py     # Semantic Classification
│   │   ├── step6_candidates.py   # Dictionary Width Matching
│   │   └── step7_consolidate.py  # Consolidation
│   └── utils/
│       └── coords.py        # Coordinate & unit conversion helpers
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── unit/                # Unit tests per module
│   ├── integration/         # End-to-end pipeline tests
│   └── fixtures/            # Test PDFs go here
├── benchmarks/              # pytest-benchmark tests
├── docs/                    # Documentation (future)
├── examples/                # Example scripts and sample output
├── pyproject.toml           # Build config, deps, tool settings
├── Makefile                 # Developer shortcuts
└── CONTRIBUTING.md          # Contributor guide
```

## Roadmap

### Phase 1 — Foundation (current)
- [x] Fat Payload schema with Pydantic validation
- [x] Pipeline orchestrator with step routing and wall-clock benchmarking
- [x] CLI with `run` and `steps` subcommands
- [x] Stub implementations for all 7 steps
- [x] Unit test scaffolding with shared fixtures
- [x] Benchmark scaffolding
- [x] Coordinate/unit conversion utilities
- [ ] Create test fixture PDFs (redacted samples with known ground truth)

### Phase 2 — Core Implementation
- [ ] **Step 1 — Ingest:** PyMuPDF integration, page dimension extraction, text layer detection, raw element extraction with normalized bboxes
- [ ] **Step 2 — Segment:** Spatial clustering algorithm (sweep-line or DBSCAN on text elements), reading-order sort, block merging
- [ ] **Step 3 — Redactions:** Black-box detection from PDF drawing commands, spatial overlap mapping to blocks, context window extraction with block boundary enforcement
- [ ] **Step 4 — Typographic:** Font frequency analysis, character-width table construction (from embedded font metrics or heuristic fallbacks), gap-width measurement (norm-to-mm), char-count range estimation
- [ ] **Step 7 — Consolidate:** Assemble RedactionResult list, graceful degradation for missing fields, JSON sink output

### Phase 3 — Intelligence Layer
- [ ] **Step 5 — Classify:** Rule-based classifier (regex on context labels, char-count heuristics), confidence scoring, extensible plugin interface for ML models
- [ ] **Step 6 — Candidates:** Dictionary/corpus loaders per data type, typographic width calculator for candidate strings, scoring function (Gaussian on width delta), top-N filtering

### Phase 4 — Hardening
- [ ] End-to-end integration tests with fixture PDFs
- [ ] Accuracy benchmarks against ground-truth datasets
- [ ] Performance profiling and optimization (especially Step 2 clustering and Step 6 dictionary matching)
- [ ] Edge cases: multi-column layouts, tables, rotated text, partial redactions, overlapping boxes
- [ ] CI/CD pipeline (lint, type-check, test matrix across Python 3.11-3.13)

### Phase 5 — Extensions
- [ ] Batch mode: process a directory of PDFs
- [ ] HTML report output (alongside JSON)
- [ ] Confidence thresholds and filtering in CLI
- [ ] Plugin system for custom classifiers and dictionary sources
- [ ] Web UI for interactive review of results

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contributor guide.

## License

MIT
