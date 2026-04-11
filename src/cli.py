"""Argument parsing and orchestration for the MusicXML → LilyPond tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from paths import INPUT_DIR, OUTPUT_DIR, iter_musicxml_files, resolve_input_path, resolve_output_directory, resolve_output_path
from pipeline import process_musicxml_to_ly


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load MusicXML, rewrite pitches (see pitch_map), write LilyPond (.ly)."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="File, or directory of .xml/.musicxml/.mxl under src/input/ if relative",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .ly path (single file), or output directory for batch; default under src/output/",
    )
    args = parser.parse_args()
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    inp = resolve_input_path(args.input)
    if inp.is_dir():
        files = iter_musicxml_files(inp)
        if not files:
            print(f"Error: no MusicXML files in {inp}", file=sys.stderr)
            if not args.input.is_absolute():
                print(f"  (relative paths are resolved under {INPUT_DIR})", file=sys.stderr)
            raise SystemExit(1)

        if args.output is not None:
            out_arg = args.output.expanduser()
            if len(files) > 1 and out_arg.suffix.lower() == ".ly":
                print(
                    "Error: with multiple inputs, --output must be a directory, not a .ly file.",
                    file=sys.stderr,
                )
                raise SystemExit(1)
            out_dir = resolve_output_directory(args.output)
        else:
            out_dir = resolve_output_directory(None)

        for f in files:
            out = out_dir / f"{f.stem}_out.ly"
            process_musicxml_to_ly(f, out)
        return

    if not inp.is_file():
        print(
            f"Error: input not found: {inp}",
            file=sys.stderr,
        )
        if not args.input.is_absolute():
            print(f"  (relative paths are resolved under {INPUT_DIR})", file=sys.stderr)
        raise SystemExit(1)

    out = resolve_output_path(args.output, inp)
    out.parent.mkdir(parents=True, exist_ok=True)
    process_musicxml_to_ly(inp, out)
