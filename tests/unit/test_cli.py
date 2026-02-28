"""Tests for the CLI argument parser."""

from __future__ import annotations

from epstein_universal_unredaction.cli import build_parser


class TestCLIParser:
    def test_run_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["run", "test.pdf"])
        assert args.command == "run"
        assert args.pdf == "test.pdf"

    def test_run_with_options(self) -> None:
        parser = build_parser()
        args = parser.parse_args([
            "run", "test.pdf",
            "--stop-after", "segment",
            "--skip", "classify,candidates",
            "-o", "out.json",
            "-vv",
        ])
        assert args.stop_after == "segment"
        assert args.skip == "classify,candidates"
        assert args.output == "out.json"
        assert args.verbose == 2

    def test_steps_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["steps"])
        assert args.command == "steps"
