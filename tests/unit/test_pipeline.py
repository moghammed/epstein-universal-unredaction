"""Tests for the pipeline orchestrator."""

from __future__ import annotations

import pytest

from epstein_universal_unredaction.pipeline import (
    _build_registry,
    create_payload,
    get_step_names,
)


class TestRegistry:
    def test_has_seven_steps(self) -> None:
        registry = _build_registry()
        assert len(registry) == 7

    def test_step_order(self) -> None:
        names = get_step_names()
        assert names == [
            "ingest",
            "segment",
            "redactions",
            "typographic",
            "classify",
            "candidates",
            "consolidate",
        ]

    def test_descriptors_have_required_fields(self) -> None:
        for step in _build_registry():
            assert step.name
            assert step.description
            assert callable(step.fn)


class TestCreatePayload:
    def test_stashes_source_path(self, tmp_path) -> None:
        pdf = tmp_path / "test.pdf"
        pdf.write_bytes(b"%PDF-1.4 fake")
        payload = create_payload(pdf)
        assert payload.__dict__["_source_pdf"] == pdf

    def test_empty_initially(self, tmp_path) -> None:
        pdf = tmp_path / "test.pdf"
        pdf.write_bytes(b"%PDF-1.4 fake")
        payload = create_payload(pdf)
        assert payload.meta is None
        assert payload.pages == []


class TestRunPipeline:
    def test_rejects_missing_file(self) -> None:
        from pathlib import Path

        from epstein_universal_unredaction.pipeline import run_pipeline

        with pytest.raises(FileNotFoundError):
            run_pipeline(Path("/nonexistent/file.pdf"))
