"""Parse MusicXML → transform → write MusicXML."""

from __future__ import annotations

import sys
from pathlib import Path

from music21 import converter

from transform import transform_score


def process_musicxml(input_path: Path, output_path: Path) -> None:
    """Load ``input_path``, run ``transform_score``, write ``output_path`` as MusicXML."""
    try:
        parsed = converter.parse(str(input_path))
    except Exception as exc:  # music21 raises various parse errors
        print(f"Error: could not parse {input_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    transform_score(parsed)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        parsed.write("musicxml", fp=str(output_path))
    except Exception as exc:
        print(f"Error: could not write {output_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Wrote {output_path}")
