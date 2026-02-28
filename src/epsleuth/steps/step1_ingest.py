"""Step 1 — Document Ingestion & Triage.

Responsibilities
----------------
* Open the source PDF (path stashed in ``payload.__dict__["_source_pdf"]``).
* Extract document-level metadata (page count, producer, creator, …).
* For every page, compute physical dimensions in **mm**, aspect ratio,
  text-layer quality, and raw text elements with normalised bounding boxes.

Writes to
---------
``payload.meta``  — :class:`~epsleuth.payload.DocumentMeta`
``payload.pages`` — list of :class:`~epsleuth.payload.PageMeta`

Implementation notes
--------------------
This stub raises ``NotImplementedError``.  The real implementation should use
*PyMuPDF* (``fitz``) or an equivalent extraction backend.  All bounding boxes
**must** be normalised to ``[0, 1]``; all physical sizes in mm.
"""

from __future__ import annotations

import logging

from epsleuth.payload import Payload

logger = logging.getLogger(__name__)


def run(payload: Payload) -> Payload:
    """Ingest the source PDF and populate triage metadata.

    Parameters
    ----------
    payload:
        Fat payload.  Must have ``_source_pdf`` stashed in ``__dict__``.

    Returns
    -------
    Payload
        The same payload with ``meta`` and ``pages`` populated.
    """
    source_pdf = payload.__dict__.get("_source_pdf")
    if source_pdf is None:
        raise RuntimeError("No _source_pdf stashed on the payload — was create_payload() used?")

    logger.debug("Ingesting %s", source_pdf)

    # TODO: Open PDF with PyMuPDF and extract:
    #   - DocumentMeta (filename, page_count, file_size_bytes, pdf_version, producer, creator)
    #   - Per-page PageMeta:
    #       - Convert page dimensions from PDF points (1pt = 1/72 in) to mm.
    #       - Compute aspect_ratio = width_mm / height_mm.
    #       - Detect text_layer quality (present / absent / partial).
    #       - Extract raw_text_elements with normalised bounding boxes.
    #         Each element dict should contain at minimum:
    #           {"text": str, "bbox": {"x": float, "y": float, "w": float, "h": float},
    #            "font": str, "size_pt": float}

    raise NotImplementedError(
        "Step 1 (ingest) is not yet implemented.  "
        "See docstring for specification."
    )
