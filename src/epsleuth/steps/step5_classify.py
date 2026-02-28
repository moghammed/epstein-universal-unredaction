"""Step 5 — Semantic Classification.

Responsibilities
----------------
* For each redaction, predict the most likely **data type** of the hidden
  content (Name, Phone, Email, Address, Date, ID Number, Monetary,
  Organisation, Unknown).
* Prediction is based on:
  - Pre/post context text (e.g. "Name: ████" → Name).
  - Gap width (e.g. a very narrow gap is unlikely to be an address).
  - Character count estimates from Step 4.

Reads from
----------
``payload.redactions_by_page``        — redaction contexts (pre/post text)
``payload.gaps_by_redaction_id``      — gap measurements
``payload.typographic_profile``       — font metrics

Writes to
---------
``payload.predictions_by_redaction_id`` — ``dict[redaction_id, SemanticPrediction]``

Implementation notes
--------------------
Initial implementation may use regex/heuristic rules on the context text.
A future version could plug in a trained classifier or LLM.
"""

from __future__ import annotations

import logging

from epsleuth.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Classify the expected data type for each redaction.

    Parameters
    ----------
    payload:
        Fat payload with redactions and gap profiles populated.

    Returns
    -------
    Payload
        The same payload with ``predictions_by_redaction_id`` populated.
    """
    if not payload.gaps_by_redaction_id:
        raise RuntimeError("No gap profiles found — was Step 4 (typographic) run?")

    logger.debug(
        "Classifying %d redaction(s)", len(payload.gaps_by_redaction_id)
    )

    # TODO: For each redaction:
    #   1. Retrieve pre_context and post_context from redactions_by_page.
    #   2. Retrieve GapProfile from gaps_by_redaction_id.
    #   3. Apply classification rules / model:
    #       - Pattern match context for labels like "Name:", "Phone:", "DOB:", …
    #       - Cross-reference estimated char count with data-type expectations
    #         (e.g. phone numbers are ~10-15 chars, emails vary widely).
    #       - Produce a RedactedDataType and a confidence score.
    #   4. Store SemanticPrediction in payload.predictions_by_redaction_id.

    raise NotImplementedError(
        "Step 5 (classify) is not yet implemented.  "
        "See docstring for specification."
    )
