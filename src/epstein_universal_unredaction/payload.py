"""Fat Payload schema.

The payload is the single mutable state dictionary that travels through the
entire pipeline.  Each step reads what it needs and writes its results under
a well-known top-level key.  Steps MUST NOT delete or overwrite keys owned
by earlier steps.

Top-level key ownership
-----------------------
Step 1 — ingest:        ``meta``, ``pages``
Step 2 — segment:       ``pages[].blocks``
Step 3 — redactions:    ``pages[].redactions``
Step 4 — typographic:   ``pages[].redactions[].gap``, ``typographic_profile``
Step 5 — classify:      ``pages[].redactions[].predicted_type``
Step 6 — candidates:    ``pages[].redactions[].candidates``
Step 7 — consolidate:   ``output``

Coordinate & unit conventions
-----------------------------
* **Normalised coords** — all ``x``, ``y``, ``w``, ``h`` values live in
  ``[0, 1]``, where ``(0, 0)`` is top-left and ``(1, 1)`` is bottom-right
  of the page.
* **Physical dims** — ``width_mm``, ``height_mm``, ``gap_width_mm`` etc.
  are in **millimetres**.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RedactedDataType(StrEnum):
    """Predicted semantic type for a redacted span."""

    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"
    DATE = "date"
    ID_NUMBER = "id_number"
    MONETARY = "monetary"
    ORGANISATION = "organisation"
    UNKNOWN = "unknown"


class TextLayerStatus(StrEnum):
    """Whether usable text was found in the PDF."""

    PRESENT = "present"
    ABSENT = "absent"
    PARTIAL = "partial"


# ---------------------------------------------------------------------------
# Nested models — coordinates & geometry
# ---------------------------------------------------------------------------

class NormalisedBox(BaseModel):
    """Axis-aligned bounding box in normalised [0, 1] coordinates."""

    x: float = Field(..., ge=0.0, le=1.0, description="Left edge (normalised).")
    y: float = Field(..., ge=0.0, le=1.0, description="Top edge (normalised).")
    w: float = Field(..., ge=0.0, le=1.0, description="Width (normalised).")
    h: float = Field(..., ge=0.0, le=1.0, description="Height (normalised).")


# ---------------------------------------------------------------------------
# Step 1 — Document Ingestion & Triage
# ---------------------------------------------------------------------------

class PageMeta(BaseModel):
    """Per-page triage metadata produced by Step 1."""

    page_number: int = Field(..., ge=0, description="Zero-indexed page number.")
    width_mm: float = Field(..., gt=0, description="Physical page width in mm.")
    height_mm: float = Field(..., gt=0, description="Physical page height in mm.")
    aspect_ratio: float = Field(..., gt=0, description="width / height.")
    text_layer: TextLayerStatus = Field(
        ..., description="Quality of the embedded text layer."
    )
    raw_text_elements: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Raw text spans extracted from the PDF.  Each dict contains at "
            "minimum ``text``, ``bbox`` (NormalisedBox-compatible dict), and "
            "``font`` information.  Exact schema depends on the extraction "
            "backend."
        ),
    )


class DocumentMeta(BaseModel):
    """Document-level triage metadata produced by Step 1."""

    filename: str
    page_count: int = Field(..., ge=1)
    file_size_bytes: int = Field(..., ge=0)
    pdf_version: str | None = None
    producer: str | None = None
    creator: str | None = None


# ---------------------------------------------------------------------------
# Step 2 — Logical Segmentation
# ---------------------------------------------------------------------------

class TextBlock(BaseModel):
    """A logical cluster of text elements with a merged bounding box."""

    block_id: str = Field(..., description="Unique block identifier within the page.")
    bbox: NormalisedBox
    text: str = Field(..., description="Concatenated text content.")
    element_indices: list[int] = Field(
        default_factory=list,
        description="Indices into ``PageMeta.raw_text_elements``.",
    )


# ---------------------------------------------------------------------------
# Step 3 — Redaction ID & Context Extraction
# ---------------------------------------------------------------------------

class RedactionContext(BaseModel):
    """A single detected redaction (black box) with its local context."""

    redaction_id: str = Field(..., description="Unique ID within the page.")
    bbox: NormalisedBox = Field(..., description="Black-box bounding box (normalised).")
    containing_block_id: str = Field(
        ..., description="ID of the TextBlock this redaction falls within."
    )
    pre_context: str = Field(
        "", description="Text immediately before the redaction, within the block."
    )
    post_context: str = Field(
        "", description="Text immediately after the redaction, within the block."
    )


# ---------------------------------------------------------------------------
# Step 4 — Typographic & Spatial Profiling
# ---------------------------------------------------------------------------

class GapProfile(BaseModel):
    """Exact metric measurement of the redacted gap."""

    gap_width_mm: float = Field(..., gt=0, description="Physical width of gap in mm.")
    gap_width_norm: float = Field(
        ..., ge=0, le=1, description="Gap width normalised to page width."
    )
    estimated_char_count_min: int = Field(
        ..., ge=0, description="Lower bound of characters that could fit."
    )
    estimated_char_count_max: int = Field(
        ..., ge=0, description="Upper bound of characters that could fit."
    )


class TypographicProfile(BaseModel):
    """Document-wide typographic rules derived in Step 4."""

    dominant_font: str | None = None
    dominant_font_size_pt: float | None = None
    mean_char_width_mm: float | None = Field(
        None, description="Average character width in mm for the dominant font."
    )
    tracking_mm: float | None = Field(
        None, description="Inter-character spacing (tracking) in mm."
    )


# ---------------------------------------------------------------------------
# Step 5 — Semantic Classification
# ---------------------------------------------------------------------------

class SemanticPrediction(BaseModel):
    """Predicted data type for a redacted gap."""

    predicted_type: RedactedDataType = RedactedDataType.UNKNOWN
    confidence: float = Field(
        0.0, ge=0.0, le=1.0, description="Model confidence in [0, 1]."
    )


# ---------------------------------------------------------------------------
# Step 6 — Dictionary Width Matching
# ---------------------------------------------------------------------------

class Candidate(BaseModel):
    """A single unredaction candidate scored against the gap width."""

    text: str
    calculated_width_mm: float = Field(
        ..., gt=0, description="Typographically calculated width in mm."
    )
    width_delta_mm: float = Field(
        ..., description="Signed difference: candidate_width - gap_width."
    )
    score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Composite match score (1.0 = perfect).",
    )


# ---------------------------------------------------------------------------
# Step 7 — Consolidation
# ---------------------------------------------------------------------------

class RedactionResult(BaseModel):
    """Final consolidated result for one redaction."""

    redaction_id: str
    page_number: int
    bbox: NormalisedBox
    pre_context: str
    post_context: str
    predicted_type: RedactedDataType
    gap_width_mm: float
    top_candidates: list[Candidate] = Field(default_factory=list)


class PipelineOutput(BaseModel):
    """Top-level output written by the consolidation step."""

    document: DocumentMeta
    results: list[RedactionResult] = Field(default_factory=list)
    pipeline_version: str = "0.1.0"


# ---------------------------------------------------------------------------
# The Fat Payload
# ---------------------------------------------------------------------------

class Payload(BaseModel):
    """The single mutable state object passed through every pipeline step.

    Fields are ``None`` / empty until the owning step populates them.
    Validators are intentionally relaxed so that partial payloads (e.g.
    after Step 1 but before Step 4) remain valid.
    """

    # Step 1
    meta: DocumentMeta | None = None
    pages: list[PageMeta] = Field(default_factory=list)

    # Step 2  — written into each PageMeta externally; tracked here for
    # convenience as a flat index.
    blocks_by_page: dict[int, list[TextBlock]] = Field(default_factory=dict)

    # Step 3
    redactions_by_page: dict[int, list[RedactionContext]] = Field(default_factory=dict)

    # Step 4
    typographic_profile: TypographicProfile | None = None
    gaps_by_redaction_id: dict[str, GapProfile] = Field(default_factory=dict)

    # Step 5
    predictions_by_redaction_id: dict[str, SemanticPrediction] = Field(
        default_factory=dict
    )

    # Step 6
    candidates_by_redaction_id: dict[str, list[Candidate]] = Field(
        default_factory=dict
    )

    # Step 7
    output: PipelineOutput | None = None

    # Benchmarking / diagnostics
    step_timings: dict[str, float] = Field(
        default_factory=dict,
        description="Wall-clock seconds keyed by step name.",
    )
