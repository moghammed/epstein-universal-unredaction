"""Integration tests — full pipeline runs.

These tests are marked ``slow`` because they exercise the entire pipeline
end-to-end and may require real PDF fixtures.  Run with:

    pytest -m slow
"""

from __future__ import annotations

import pytest


@pytest.mark.slow
class TestFullPipeline:
    """Placeholder for end-to-end pipeline tests.

    Once step implementations land, add tests here that:
    1. Run run_pipeline() on a fixture PDF.
    2. Assert payload.output is populated.
    3. Spot-check known redactions in the fixture.
    """

    def test_placeholder(self) -> None:
        # Remove this once real integration tests exist.
        pytest.skip("No step implementations yet — nothing to integrate.")
