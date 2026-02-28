"""Step 6 — Dictionary Width Matching.

Responsibilities
----------------
* For each redaction, generate a list of **candidate replacement strings**
  from a dictionary / data source appropriate to the predicted type.
* Calculate the **typographic width** of each candidate (in mm) using the
  font metrics from Step 4.
* Score each candidate by how closely its width matches the physical gap
  width, producing a ranked list.

Reads from
----------
``payload.redactions_by_page``          — redaction contexts
``payload.gaps_by_redaction_id``        — gap measurements
``payload.predictions_by_redaction_id`` — predicted data types
``payload.typographic_profile``         — font metrics for width calculation

Writes to
---------
``payload.candidates_by_redaction_id`` — ``dict[redaction_id, list[Candidate]]``

Implementation notes
--------------------
Width calculation should use the same font-metric source as Step 4 for
consistency.  Candidates might come from name databases, phone format
generators, email pattern generators, etc. depending on the predicted type.
"""

from __future__ import annotations

import logging

from epstein_universal_unredaction.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Generate and score candidate strings for each redaction.

    Parameters
    ----------
    payload:
        Fat payload with gap profiles and semantic predictions populated.

    Returns
    -------
    Payload
        The same payload with ``candidates_by_redaction_id`` populated.
    """
    if not payload.predictions_by_redaction_id:
        raise RuntimeError("No predictions found — was Step 5 (classify) run?")

    logger.debug(
        "Generating candidates for %d redaction(s)",
        len(payload.predictions_by_redaction_id),
    )

    # TODO: For each redaction:
    #   1. Look up predicted_type from predictions_by_redaction_id.
    #   2. Select a candidate source appropriate to that type:
    #       - NAME → name dictionary / census data
    #       - PHONE → phone format generator for relevant locale
    #       - EMAIL → pattern-based email generator
    #       - ADDRESS → address corpus
    #       - DATE → date format generator
    #       - ID_NUMBER → format-based generator (SSN, passport, etc.)
    #       - MONETARY → currency format generator
    #       - ORGANISATION → org-name corpus
    #       - UNKNOWN → broad dictionary
    #   3. For each candidate string:
    #       a. Calculate typographic width (mm) using font metrics.
    #          width = sum(char_widths) + (len - 1) * tracking_mm
    #       b. Compute width_delta_mm = candidate_width - gap_width_mm.
    #       c. Compute score (e.g. Gaussian falloff on |width_delta_mm|).
    #       d. Build Candidate object.
    #   4. Sort by score descending, keep top N.
    #   5. Store in payload.candidates_by_redaction_id[redaction_id].

    raise NotImplementedError(
        "Step 6 (candidates) is not yet implemented.  "
        "See docstring for specification."
    )
