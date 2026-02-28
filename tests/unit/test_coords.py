"""Tests for coordinate / unit conversion helpers."""

from __future__ import annotations

import pytest

from epsleuth.utils.coords import (
    denormalise_to_mm,
    mm_to_pts,
    normalise,
    pts_to_mm,
)


class TestPtsToMm:
    def test_known_value(self) -> None:
        # 72 pts == 1 inch == 25.4 mm
        assert pts_to_mm(72.0) == pytest.approx(25.4)

    def test_zero(self) -> None:
        assert pts_to_mm(0.0) == 0.0


class TestMmToPts:
    def test_round_trip(self) -> None:
        assert mm_to_pts(pts_to_mm(100.0)) == pytest.approx(100.0)


class TestNormalise:
    def test_midpoint(self) -> None:
        assert normalise(50.0, 100.0) == pytest.approx(0.5)

    def test_clamps_to_zero(self) -> None:
        assert normalise(-10.0, 100.0) == 0.0

    def test_clamps_to_one(self) -> None:
        assert normalise(150.0, 100.0) == 1.0

    def test_rejects_non_positive_extent(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            normalise(50.0, 0.0)


class TestDenormaliseToMm:
    def test_full_width(self) -> None:
        assert denormalise_to_mm(1.0, 210.0) == pytest.approx(210.0)

    def test_half_width(self) -> None:
        assert denormalise_to_mm(0.5, 210.0) == pytest.approx(105.0)
