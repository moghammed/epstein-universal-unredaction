"""Command-line interface for epsleuth.

Usage::

    epsleuth run document.pdf
    epsleuth run document.pdf --stop-after segment
    epsleuth run document.pdf --output results.json
    epsleuth steps                # list available steps
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from epsleuth import __version__


def _configure_logging(verbosity: int) -> None:
    level = {0: logging.WARNING, 1: logging.INFO}.get(verbosity, logging.DEBUG)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )


def _cmd_run(args: argparse.Namespace) -> int:
    """Execute the pipeline on a PDF."""
    from epsleuth.pipeline import run_pipeline

    _configure_logging(args.verbose)

    pdf_path = Path(args.pdf)
    if not pdf_path.is_file():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        return 1

    skip = set(args.skip.split(",")) if args.skip else None

    try:
        payload = run_pipeline(
            pdf_path,
            stop_after=args.stop_after,
            skip=skip,
        )
    except NotImplementedError as exc:
        print(f"Pipeline halted (unimplemented step): {exc}", file=sys.stderr)
        return 2

    # Emit output
    if payload.output is not None:
        result_json = payload.output.model_dump_json(indent=2)
    else:
        # Partial run — dump step_timings as a diagnostic.
        result_json = json.dumps(
            {"step_timings": payload.step_timings, "note": "partial run — no consolidated output"},
            indent=2,
        )

    if args.output:
        Path(args.output).write_text(result_json, encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(result_json)

    # Print timing summary
    if payload.step_timings:
        print("\n--- Timing Summary ---", file=sys.stderr)
        for step_name, elapsed in payload.step_timings.items():
            if step_name == "__total__":
                continue
            print(f"  {step_name:20s}  {elapsed:.4f}s", file=sys.stderr)
        total = payload.step_timings.get("__total__")
        if total is not None:
            print(f"  {'TOTAL':20s}  {total:.4f}s", file=sys.stderr)

    return 0


def _cmd_steps(_args: argparse.Namespace) -> int:
    """Print the ordered list of pipeline steps."""
    from epsleuth.pipeline import _build_registry

    for i, step in enumerate(_build_registry(), 1):
        print(f"  {i}. {step.name:15s} — {step.description}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="epsleuth",
        description="Unredaction pipeline for PDF documents.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    # --- run ---
    run_p = sub.add_parser("run", help="Run the pipeline on a PDF.")
    run_p.add_argument("pdf", help="Path to the input PDF.")
    run_p.add_argument(
        "-o", "--output",
        help="Write JSON output to this file instead of stdout.",
    )
    run_p.add_argument(
        "--stop-after",
        metavar="STEP",
        help="Stop after the named step (e.g. 'segment').",
    )
    run_p.add_argument(
        "--skip",
        metavar="STEPS",
        help="Comma-separated step names to skip.",
    )
    run_p.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v info, -vv debug).",
    )
    run_p.set_defaults(func=_cmd_run)

    # --- steps ---
    steps_p = sub.add_parser("steps", help="List pipeline steps.")
    steps_p.set_defaults(func=_cmd_steps)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
