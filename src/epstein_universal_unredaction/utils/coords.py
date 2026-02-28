"""Coordinate and unit conversion helpers.

All public functions in this module deal with the two coordinate systems
used throughout the pipeline:

* **Normalised** — ``[0, 1]`` relative to page dimensions.
* **Physical** — millimetres (mm).

Constants
---------
PT_TO_MM : float
    1 PDF point = 1/72 inch = 0.352778 mm.
"""

from __future__ import annotations

PT_TO_MM: float = 25.4 / 72.0  # ≈ 0.352778


def pts_to_mm(pts: float) -> float:
    """Convert PDF points to millimetres."""
    return pts * PT_TO_MM


def mm_to_pts(mm: float) -> float:
    """Convert millimetres to PDF points."""
    return mm / PT_TO_MM


def normalise(value: float, page_extent: float) -> float:
    """Normalise *value* (in any unit) by *page_extent* (same unit).

    Returns a float clamped to ``[0, 1]``.
    """
    if page_extent <= 0:
        raise ValueError(f"page_extent must be positive, got {page_extent}")
    return max(0.0, min(1.0, value / page_extent))


def denormalise_to_mm(norm: float, page_extent_mm: float) -> float:
    """Convert a normalised ``[0, 1]`` value back to mm."""
    return norm * page_extent_mm
