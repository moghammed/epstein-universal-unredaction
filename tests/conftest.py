"""Shared test fixtures for epsleuth."""

from __future__ import annotations

from pathlib import Path

import pytest

from epsleuth.payload import (
    Candidate,
    DocumentMeta,
    GapProfile,
    NormalisedBox,
    PageMeta,
    Payload,
    RedactedDataType,
    RedactionContext,
    SemanticPrediction,
    TextBlock,
    TextLayerStatus,
    TypographicProfile,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fixtures_dir() -> Path:
    """Path to the test fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture()
def sample_document_meta() -> DocumentMeta:
    return DocumentMeta(
        filename="test.pdf",
        page_count=2,
        file_size_bytes=102_400,
        pdf_version="1.7",
        producer="Test Producer",
    )


@pytest.fixture()
def sample_page_meta() -> PageMeta:
    return PageMeta(
        page_number=0,
        width_mm=210.0,
        height_mm=297.0,
        aspect_ratio=210.0 / 297.0,
        text_layer=TextLayerStatus.PRESENT,
        raw_text_elements=[
            {
                "text": "Name:",
                "bbox": {"x": 0.1, "y": 0.1, "w": 0.08, "h": 0.02},
                "font": "Helvetica",
                "size_pt": 12.0,
            },
            {
                "text": "is a resident",
                "bbox": {"x": 0.4, "y": 0.1, "w": 0.15, "h": 0.02},
                "font": "Helvetica",
                "size_pt": 12.0,
            },
        ],
    )


@pytest.fixture()
def sample_block() -> TextBlock:
    return TextBlock(
        block_id="p0_b0",
        bbox=NormalisedBox(x=0.1, y=0.1, w=0.45, h=0.02),
        text="Name: ████ is a resident",
        element_indices=[0, 1],
    )


@pytest.fixture()
def sample_redaction() -> RedactionContext:
    return RedactionContext(
        redaction_id="p0_r0",
        bbox=NormalisedBox(x=0.19, y=0.1, w=0.2, h=0.02),
        containing_block_id="p0_b0",
        pre_context="Name:",
        post_context="is a resident",
    )


@pytest.fixture()
def sample_gap() -> GapProfile:
    return GapProfile(
        gap_width_mm=42.0,
        gap_width_norm=0.2,
        estimated_char_count_min=10,
        estimated_char_count_max=18,
    )


@pytest.fixture()
def sample_typographic_profile() -> TypographicProfile:
    return TypographicProfile(
        dominant_font="Helvetica",
        dominant_font_size_pt=12.0,
        mean_char_width_mm=2.8,
        tracking_mm=0.1,
    )


@pytest.fixture()
def sample_prediction() -> SemanticPrediction:
    return SemanticPrediction(
        predicted_type=RedactedDataType.NAME,
        confidence=0.85,
    )


@pytest.fixture()
def sample_candidate() -> Candidate:
    return Candidate(
        text="John Smith",
        calculated_width_mm=41.5,
        width_delta_mm=-0.5,
        score=0.95,
    )


@pytest.fixture()
def empty_payload() -> Payload:
    """A fresh, completely empty payload."""
    return Payload()


@pytest.fixture()
def payload_after_step1(
    sample_document_meta: DocumentMeta,
    sample_page_meta: PageMeta,
) -> Payload:
    """Payload as it would look after Step 1 (ingest)."""
    return Payload(
        meta=sample_document_meta,
        pages=[sample_page_meta],
    )
