"""Pipeline orchestrator.

Owns the ordered registry of steps, the routing logic that passes the fat
payload through each step sequentially, and per-step wall-clock benchmarking.

Usage::

    from pathlib import Path
    from epstein_universal_unredaction.pipeline import run_pipeline

    output = run_pipeline(Path("document.pdf"))
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from epstein_universal_unredaction.payload import Payload

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Step protocol — every step module must expose a function with this shape.
# ---------------------------------------------------------------------------

class StepFn(Protocol):
    """Callable signature that every pipeline step must satisfy."""

    def __call__(self, payload: Payload) -> Payload: ...


# ---------------------------------------------------------------------------
# Step descriptor
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class StepDescriptor:
    """Metadata for a single pipeline step."""

    name: str
    description: str
    fn: StepFn
    # Optional hooks for future extensibility (e.g. pre/post validation).
    pre_hooks: list[Callable[[Payload], None]] = field(default_factory=list)
    post_hooks: list[Callable[[Payload], None]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Registry — import each step's entry-point and declare ordering.
# ---------------------------------------------------------------------------

def _build_registry() -> list[StepDescriptor]:
    """Lazily import step modules and return the ordered registry.

    Lazy imports keep startup fast and let contributors work on one step
    without needing every dependency installed.
    """
    from epstein_universal_unredaction.steps.step1_ingest import run as ingest
    from epstein_universal_unredaction.steps.step2_segment import run as segment
    from epstein_universal_unredaction.steps.step3_redactions import run as redactions
    from epstein_universal_unredaction.steps.step4_typographic import run as typographic
    from epstein_universal_unredaction.steps.step5_classify import run as classify
    from epstein_universal_unredaction.steps.step6_candidates import run as candidates
    from epstein_universal_unredaction.steps.step7_consolidate import run as consolidate

    return [
        StepDescriptor(
            name="ingest",
            description="Document Ingestion & Triage",
            fn=ingest,
        ),
        StepDescriptor(
            name="segment",
            description="Logical Segmentation",
            fn=segment,
        ),
        StepDescriptor(
            name="redactions",
            description="Redaction ID & Context Extraction",
            fn=redactions,
        ),
        StepDescriptor(
            name="typographic",
            description="Typographic & Spatial Profiling",
            fn=typographic,
        ),
        StepDescriptor(
            name="classify",
            description="Semantic Classification",
            fn=classify,
        ),
        StepDescriptor(
            name="candidates",
            description="Dictionary Width Matching",
            fn=candidates,
        ),
        StepDescriptor(
            name="consolidate",
            description="Consolidation",
            fn=consolidate,
        ),
    ]


# ---------------------------------------------------------------------------
# Execution helpers
# ---------------------------------------------------------------------------

def _execute_step(step: StepDescriptor, payload: Payload) -> Payload:
    """Run a single step with timing, logging, and hook execution."""
    logger.info("┌─ Step [%s]: %s", step.name, step.description)

    for hook in step.pre_hooks:
        hook(payload)

    t0 = time.perf_counter()
    payload = step.fn(payload)
    elapsed = time.perf_counter() - t0

    payload.step_timings[step.name] = elapsed

    for hook in step.post_hooks:
        hook(payload)

    logger.info("└─ Step [%s] completed in %.4fs", step.name, elapsed)
    return payload


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_payload(pdf_path: Path) -> Payload:
    """Initialise a fresh payload seeded with the input PDF path.

    The *ingest* step will read the file and populate ``meta`` and ``pages``.
    We store the path in a private stash so Step 1 can find it without
    polluting the public schema.
    """
    payload = Payload()
    # Stash the source path for the ingest step.  We use model_config
    # extra='allow' would be one option, but a simple annotation-free
    # attribute is cleaner for a "bag of state".
    payload.__dict__["_source_pdf"] = pdf_path
    return payload


def run_pipeline(
    pdf_path: Path,
    *,
    stop_after: str | None = None,
    skip: set[str] | None = None,
) -> Payload:
    """Execute the full (or partial) pipeline on *pdf_path*.

    Parameters
    ----------
    pdf_path:
        Path to the input PDF document.
    stop_after:
        If given, halt after the named step (e.g. ``"segment"``).
    skip:
        Set of step names to skip entirely.  Use with caution — later steps
        may depend on data produced by earlier ones.

    Returns
    -------
    Payload
        The enriched payload after all executed steps.
    """
    pdf_path = Path(pdf_path).expanduser().resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    payload = create_payload(pdf_path)
    registry = _build_registry()
    skip = skip or set()

    total_t0 = time.perf_counter()

    for step in registry:
        if step.name in skip:
            logger.info("⏭  Skipping step [%s]", step.name)
            continue

        payload = _execute_step(step, payload)

        if stop_after and step.name == stop_after:
            logger.info("⏹  Stopping after step [%s] as requested.", step.name)
            break

    total_elapsed = time.perf_counter() - total_t0
    payload.step_timings["__total__"] = total_elapsed
    logger.info("Pipeline finished in %.4fs", total_elapsed)

    return payload


def get_step_names() -> list[str]:
    """Return the ordered list of step names (useful for CLI help)."""
    return [s.name for s in _build_registry()]
