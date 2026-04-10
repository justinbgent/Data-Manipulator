"""Read MusicXML, transform with music21, write MusicXML."""

#   Put MusicXML files in src\input\, then:
#   python src\main.py -i piece.musicxml
#   python src\main.py -i piece.musicxml -o edited.musicxml
#
# Relative -i is under src\input\; relative -o (or default) is under src\output\ (<stem>_out.musicxml).
# Absolute -i/-o use those paths. Flow: parse → transform_score() → write MusicXML.
# Missing output dirs are created; parse/write errors → stderr, exit 1.

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from music21 import converter, stream

_SRC_DIR = Path(__file__).resolve().parent
INPUT_DIR = _SRC_DIR / "input"
OUTPUT_DIR = _SRC_DIR / "output"


def _resolve_input_path(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (INPUT_DIR / path).resolve()


def _resolve_output_path(out_arg: Path | None, input_path: Path) -> Path:
    if out_arg is None:
        return (OUTPUT_DIR / f"{input_path.stem}_out.musicxml").resolve()
    out_arg = out_arg.expanduser()
    if out_arg.is_absolute():
        return out_arg.resolve()
    return (OUTPUT_DIR / out_arg).resolve()


def transform_score(score: stream.Stream) -> None:
    """Modify the parsed stream in place before writing.

    Customize this function for your edits (transpose, fix spelling, split parts, etc.).
    """
    # Example (disabled): transpose up a major second
    # score.transpose(2, inPlace=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load a MusicXML file, edit it with music21, and write a new MusicXML file."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Input file under src/input/ if relative (.xml, .musicxml, or .mxl)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .musicxml under src/output/ if relative (default: <input_stem>_out.musicxml)",
    )
    args = parser.parse_args()
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    inp = _resolve_input_path(args.input)
    if not inp.is_file():
        print(
            f"Error: input not found: {inp}",
            file=sys.stderr,
        )
        if not args.input.is_absolute():
            print(f"  (relative paths are resolved under {INPUT_DIR})", file=sys.stderr)
        raise SystemExit(1)

    out = _resolve_output_path(args.output, inp)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        parsed = converter.parse(str(inp))
    except Exception as exc:  # music21 raises various parse errors
        print(f"Error: could not parse {inp}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    transform_score(parsed)

    try:
        parsed.write("musicxml", fp=str(out))
    except Exception as exc:
        print(f"Error: could not write {out}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()


# Relative -i paths are read from src\input\. Relative -o paths are written under src\output\.
# Use absolute paths for -i or -o to read/write anywhere else.
# Default output if -o omitted: src\output\<input_stem>_out.musicxml
# Customize edits in transform_score() below.
#
# How the program works:
#   1. -i/--input: MusicXML file (.xml, .musicxml, or .mxl); relative names use src\input\.
#   2. music21 converter.parse() loads the file into a stream (Score, Part, etc.).
#   3. transform_score() edits that stream in place (empty by default; add your logic there).
#   4. The stream is written with write("musicxml", fp=...) to a new MusicXML file.
#   5. -o/--output is optional; relative paths go under src\output\; default output name
#      is <input_stem>_out.musicxml in src\output\.
#   If the output directory does not exist, it is created. Parse/write errors go to stderr
#   and the program exits with status 1.

# MusicXML pitch element:
# <pitch>
#   <step>C</step>
#   <octave>4</octave>
#   <alter>0</alter>
# </pitch>

# C on 4th octave is middle C.
# alter values are -1, 0, 1 for -1 half step, 0 no change, 1 half step.
# Or in other words, -1 is a flat, 0 is a natural, 1 is a sharp.

# On treble clef, the notes are as follows:
# C4 will map to D4,
# C#4 to E4,
# D4 to F4,
# D#4 to G4,
# E4 to A4,
# F4 to B4,
# F#4 to C5,
# G4 to D5,
# G#4 to E5,
# A4 to F5,
# A#4 to G5,
# B4 to A5,

# Note what I am describe visually will look like how the piano is layed out. Black lines for
# sharps/flats, white spaces for naturals. The goal is to make it more intuitive for which
# key to press.

# Treble clef pattern:
# Sharps/Flats will fall on staff lines, naturals will fall in white spaces between lines.
# In Lily Pond, the treble clef lines will be -4, -2, 1, 3, 5.
# Lines not shown, white spaces are naturals: -5(C4), -3(D4), -1(E4), 0(F4), 2(G4), 4(A4), 6(B4)
# This pattern will repeat for each octave. And now sharps and flats have dedicated positions.

# Todo: Base Clef pattern.

# Midi pitch values. Not used for music xml.
# C4 is pitch 60
# C#4: 61
# D4: 62
# D#4: 63
# E4: 64
# F4: 65
# F#4: 66
# G4: 67
# G#4: 68
# A4: 69
# A#4: 70
# B4: 71
# C5: 72