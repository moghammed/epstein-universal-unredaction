"""epstein-universal-unredaction — Unredaction pipeline for PDF documents.

Reverse-engineers black-box redactions using spatial and typographic
analysis.  The pipeline passes a single "fat payload" dictionary through
seven sequential steps, each one enriching the payload with new data.

Coordinate convention:
    All spatial coordinates are normalized to [0, 1] relative to page
    dimensions.  Physical measurements (page size, gap widths, etc.) are
    expressed in millimeters (mm).
"""

__version__ = "0.1.0"
