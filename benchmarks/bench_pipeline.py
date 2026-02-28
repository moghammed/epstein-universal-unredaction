"""Benchmarks for individual pipeline steps and the full pipeline.

Run with:
    pytest benchmarks/ -m benchmark --benchmark-enable

These benchmarks use pytest-benchmark and will only produce meaningful
results once step implementations are in place.  Until then they serve
as the scaffolding contributors should use.
"""

from __future__ import annotations

import pytest

from epsleuth.payload import (
    DocumentMeta,
    PageMeta,
    Payload,
    TextLayerStatus,
)


def _make_payload_with_pages(n_pages: int, elements_per_page: int) -> Payload:
    """Build a synthetic payload for benchmarking."""
    pages = []
    for i in range(n_pages):
        elements = [
            {
                "text": f"word_{j}",
                "bbox": {"x": 0.05 * (j % 20), "y": 0.05 * (j // 20), "w": 0.04, "h": 0.02},
                "font": "Helvetica",
                "size_pt": 12.0,
            }
            for j in range(elements_per_page)
        ]
        pages.append(
            PageMeta(
                page_number=i,
                width_mm=210.0,
                height_mm=297.0,
                aspect_ratio=210.0 / 297.0,
                text_layer=TextLayerStatus.PRESENT,
                raw_text_elements=elements,
            )
        )
    return Payload(
        meta=DocumentMeta(
            filename="bench.pdf",
            page_count=n_pages,
            file_size_bytes=n_pages * 50_000,
        ),
        pages=pages,
    )


@pytest.mark.benchmark
class TestPayloadSerialization:
    """Benchmark payload (de)serialisation — a hot path in any pipeline run."""

    def test_serialize_small(self, benchmark) -> None:
        payload = _make_payload_with_pages(5, 50)
        benchmark(payload.model_dump_json)

    def test_serialize_large(self, benchmark) -> None:
        payload = _make_payload_with_pages(50, 200)
        benchmark(payload.model_dump_json)

    def test_deserialize_small(self, benchmark) -> None:
        payload = _make_payload_with_pages(5, 50)
        json_bytes = payload.model_dump_json()
        benchmark(Payload.model_validate_json, json_bytes)


# Add per-step benchmarks below once implementations exist.
# Example:
#
# @pytest.mark.benchmark
# class TestStep2Segment:
#     def test_segment_10_pages(self, benchmark) -> None:
#         payload = _make_payload_with_pages(10, 100)
#         from epsleuth.steps.step2_segment import run
#         benchmark(run, payload)
