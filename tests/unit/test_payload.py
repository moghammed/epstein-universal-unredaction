"""Tests for the payload schema and model validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from epstein_universal_unredaction.payload import (
    Candidate,
    DocumentMeta,
    GapProfile,
    NormalisedBox,
    PageMeta,
    Payload,
    RedactedDataType,
    SemanticPrediction,
    TextLayerStatus,
)


class TestNormalisedBox:
    def test_valid_box(self) -> None:
        box = NormalisedBox(x=0.1, y=0.2, w=0.3, h=0.4)
        assert box.x == 0.1
        assert box.w == 0.3

    def test_boundary_values(self) -> None:
        box = NormalisedBox(x=0.0, y=0.0, w=1.0, h=1.0)
        assert box.x == 0.0
        assert box.h == 1.0

    def test_rejects_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            NormalisedBox(x=-0.1, y=0.0, w=0.5, h=0.5)
        with pytest.raises(ValidationError):
            NormalisedBox(x=0.0, y=0.0, w=1.1, h=0.5)


class TestDocumentMeta:
    def test_valid(self, sample_document_meta: DocumentMeta) -> None:
        assert sample_document_meta.page_count == 2

    def test_rejects_zero_pages(self) -> None:
        with pytest.raises(ValidationError):
            DocumentMeta(filename="bad.pdf", page_count=0, file_size_bytes=100)


class TestPageMeta:
    def test_valid(self, sample_page_meta: PageMeta) -> None:
        assert sample_page_meta.width_mm == 210.0
        assert sample_page_meta.text_layer == TextLayerStatus.PRESENT

    def test_raw_text_elements_default(self) -> None:
        page = PageMeta(
            page_number=0,
            width_mm=100.0,
            height_mm=100.0,
            aspect_ratio=1.0,
            text_layer=TextLayerStatus.ABSENT,
        )
        assert page.raw_text_elements == []


class TestGapProfile:
    def test_valid(self, sample_gap: GapProfile) -> None:
        assert sample_gap.gap_width_mm == 42.0
        assert sample_gap.estimated_char_count_min <= sample_gap.estimated_char_count_max


class TestCandidate:
    def test_valid(self, sample_candidate: Candidate) -> None:
        assert sample_candidate.score >= 0.0
        assert sample_candidate.score <= 1.0

    def test_rejects_bad_score(self) -> None:
        with pytest.raises(ValidationError):
            Candidate(
                text="x",
                calculated_width_mm=10.0,
                width_delta_mm=0.0,
                score=1.5,
            )


class TestSemanticPrediction:
    def test_defaults(self) -> None:
        pred = SemanticPrediction()
        assert pred.predicted_type == RedactedDataType.UNKNOWN
        assert pred.confidence == 0.0


class TestPayload:
    def test_empty_payload(self, empty_payload: Payload) -> None:
        assert empty_payload.meta is None
        assert empty_payload.pages == []
        assert empty_payload.output is None
        assert empty_payload.step_timings == {}

    def test_partial_payload(self, payload_after_step1: Payload) -> None:
        assert payload_after_step1.meta is not None
        assert len(payload_after_step1.pages) == 1
        # Later steps haven't run yet.
        assert payload_after_step1.typographic_profile is None
        assert payload_after_step1.output is None

    def test_round_trip_json(self, payload_after_step1: Payload) -> None:
        json_str = payload_after_step1.model_dump_json()
        restored = Payload.model_validate_json(json_str)
        assert restored.meta == payload_after_step1.meta
        assert len(restored.pages) == len(payload_after_step1.pages)
