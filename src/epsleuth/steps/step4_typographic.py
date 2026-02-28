"""Step 4 — Typographic & Spatial Profiling.

Responsibilities
----------------
* Derive a document-wide typographic profile: dominant font, font size,
  mean character width (mm), inter-character tracking (mm).
* For each redaction, compute the **exact physical width** of the gap in
  mm and estimate a character-count range.

Reads from
----------
``payload.pages``              — raw text elements (font / size info)
``payload.redactions_by_page`` — detected redactions from Step 3

Writes to
---------
``payload.typographic_profile``   — :class:`~epsleuth.payload.TypographicProfile`
``payload.gaps_by_redaction_id``  — ``dict[redaction_id, GapProfile]``

Implementation notes
--------------------
Character width estimation can use font metrics from the PDF (if embedded)
or fall back to heuristic tables for common fonts.  Gap width must be
converted from normalised coordinates to mm using the page's physical
dimensions.
"""

from __future__ import annotations

import logging

from epsleuth.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Build typographic profile and measure redaction gaps.

    Parameters
    ----------
    payload:
        Fat payload with ``pages`` and ``redactions_by_page`` populated.

    Returns
    -------
    Payload
        The same payload with ``typographic_profile`` and
        ``gaps_by_redaction_id`` populated.
    """
    if not payload.redactions_by_page:
        raise RuntimeError("No redactions found — was Step 3 (redactions) run?")

    logger.debug("Profiling typography")

    # TODO:
    #   1. Global typographic profile:
    #       a. Tally font names and sizes across all raw_text_elements.
    #       b. Identify dominant_font and dominant_font_size_pt.
    #       c. Compute mean_char_width_mm:
    #          For each text element, width_mm / len(text) → average.
    #       d. Estimate tracking_mm (inter-character spacing) by comparing
    #          measured span widths to expected glyph-only widths.
    #       e. Populate payload.typographic_profile.
    #
    #   2. Per-redaction gap measurement:
    #       For each redaction in redactions_by_page:
    #       a. Convert bbox.w (normalised) → physical mm using page width_mm.
    #       b. Estimate character count range:
    #          min_chars = floor(gap_width_mm / max_char_width_mm)
    #          max_chars = ceil(gap_width_mm / min_char_width_mm)
    #       c. Build GapProfile and store in payload.gaps_by_redaction_id.

    raise NotImplementedError(
        "Step 4 (typographic) is not yet implemented.  "
        "See docstring for specification."
    )
