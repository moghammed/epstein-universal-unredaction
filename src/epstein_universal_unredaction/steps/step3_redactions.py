"""Step 3 — Redaction Identification & Context Extraction.

Responsibilities
----------------
* Scan each page for filled black rectangles (the redaction boxes).
* Map each black box to its containing logical block (from Step 2).
* Extract the **pre-context** and **post-context** text strictly within that
  block — i.e. the text immediately before and after the redaction box,
  limited to the block boundary.

Reads from
----------
``payload.pages``          — raw page data
``payload.blocks_by_page`` — logical blocks from Step 2

Writes to
---------
``payload.redactions_by_page`` — ``dict[page_number, list[RedactionContext]]``

Implementation notes
--------------------
Black-box detection typically examines PDF drawing commands for filled
rectangles with RGB (0, 0, 0).  Context extraction must respect block
boundaries so that text from neighbouring blocks is never mixed in.
"""

from __future__ import annotations

import logging

from epstein_universal_unredaction.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Locate redaction boxes and extract their local context.

    Parameters
    ----------
    payload:
        Fat payload with ``pages`` and ``blocks_by_page`` populated.

    Returns
    -------
    Payload
        The same payload with ``redactions_by_page`` populated.
    """
    if not payload.blocks_by_page:
        raise RuntimeError("No blocks found — was Step 2 (segment) run?")

    logger.debug("Detecting redactions across %d page(s)", len(payload.pages))

    # TODO: For each page:
    #   1. Identify filled black rectangles (potential redactions).
    #      - Look at PDF drawing operations / annotations.
    #      - Normalise their bounding boxes to [0, 1].
    #   2. For each black box:
    #       a. Find the containing TextBlock by checking spatial overlap
    #          with blocks_by_page[page_number].
    #       b. Within that block's raw_text_elements (via element_indices),
    #          find text elements immediately to the left → pre_context,
    #          and immediately to the right → post_context.
    #       c. Build a RedactionContext(redaction_id, bbox,
    #          containing_block_id, pre_context, post_context).
    #   3. Store result in payload.redactions_by_page[page_number].

    raise NotImplementedError(
        "Step 3 (redactions) is not yet implemented.  "
        "See docstring for specification."
    )
