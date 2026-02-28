"""Step 2 — Logical Segmentation.

Responsibilities
----------------
* Read ``payload.pages[].raw_text_elements``.
* Cluster spatially adjacent text elements into logical blocks (paragraphs,
  table cells, headers, etc.) using proximity heuristics.
* Assign each block a merged normalised bounding box and concatenated text.

Reads from
----------
``payload.pages`` — specifically ``raw_text_elements`` on each page.

Writes to
---------
``payload.blocks_by_page`` — ``dict[page_number, list[TextBlock]]``

Implementation notes
--------------------
Clustering can be as simple as a greedy sweep-line that groups elements
whose vertical overlap exceeds a threshold, or as sophisticated as a
learned layout model.  The stub raises ``NotImplementedError``.
"""

from __future__ import annotations

import logging

from epstein_universal_unredaction.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Cluster raw text elements into logical blocks.

    Parameters
    ----------
    payload:
        Fat payload with ``pages`` populated by Step 1.

    Returns
    -------
    Payload
        The same payload with ``blocks_by_page`` populated.
    """
    if not payload.pages:
        raise RuntimeError("No pages found — was Step 1 (ingest) run?")

    logger.debug("Segmenting %d page(s)", len(payload.pages))

    # TODO: For each page in payload.pages:
    #   1. Read raw_text_elements.
    #   2. Cluster elements into logical blocks using spatial proximity.
    #      Consider: vertical overlap, horizontal gap, font consistency.
    #   3. For each cluster:
    #       - Compute merged NormalisedBox (min x/y, max x+w/y+h).
    #       - Concatenate text in reading order.
    #       - Record element_indices (pointers back into raw_text_elements).
    #       - Assign a unique block_id (e.g. "p0_b0", "p0_b1", …).
    #   4. Store result in payload.blocks_by_page[page_number].

    raise NotImplementedError(
        "Step 2 (segment) is not yet implemented.  "
        "See docstring for specification."
    )
