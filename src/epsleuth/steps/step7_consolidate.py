"""Step 7 — Consolidation.

Responsibilities
----------------
* Collect results from all previous steps into a clean, human-reviewable
  output structure.
* Build the final :class:`~epsleuth.payload.PipelineOutput` containing
  one :class:`~epsleuth.payload.RedactionResult` per redaction.
* Optionally serialise the output to a JSON file (the "sink").

Reads from
----------
All prior payload fields.

Writes to
---------
``payload.output`` — :class:`~epsleuth.payload.PipelineOutput`

Implementation notes
--------------------
This step should never fail on missing data; it should gracefully degrade
(e.g. if no candidates exist for a redaction, ``top_candidates`` is empty).
"""

from __future__ import annotations

import logging

from epsleuth.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Consolidate all pipeline results into the final output.

    Parameters
    ----------
    payload:
        Fully enriched fat payload.

    Returns
    -------
    Payload
        The same payload with ``output`` populated.
    """
    logger.debug("Consolidating results")

    # TODO:
    #   1. Iterate over all redactions across all pages.
    #   2. For each redaction:
    #       a. Look up GapProfile from gaps_by_redaction_id.
    #       b. Look up SemanticPrediction from predictions_by_redaction_id.
    #       c. Look up Candidates from candidates_by_redaction_id.
    #       d. Build RedactionResult:
    #           - redaction_id, page_number, bbox
    #           - pre_context, post_context
    #           - predicted_type (from prediction or UNKNOWN)
    #           - gap_width_mm (from gap profile or 0.0)
    #           - top_candidates (sorted by score, top N)
    #   3. Build PipelineOutput:
    #       - document = payload.meta
    #       - results = list of all RedactionResult
    #       - pipeline_version = epsleuth.__version__
    #   4. Assign to payload.output.

    raise NotImplementedError(
        "Step 7 (consolidate) is not yet implemented.  "
        "See docstring for specification."
    )
