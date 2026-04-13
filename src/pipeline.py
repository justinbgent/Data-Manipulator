"""Parse MusicXML → transform → write LilyPond source."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from music21 import converter, environment

from paths import BUNDLED_LILYPOND
from transform import transform_score

try:
    from music21.lily.translate import LilyTranslateException as _LilyTranslateException
except ImportError:  # pragma: no cover
    # Do not fall back to ``Exception`` — that would label every write failure
    # as a LilyPond install issue. When missing, only the generic branch runs.
    _LilyTranslateException = None


def _configure_lilypond_path() -> None:
    """Prefer ``LILYPOND_PATH``, then repo-bundled Windows binary; else music21 defaults."""
    us = environment.UserSettings()
    env_path = os.environ.get("LILYPOND_PATH", "").strip()
    if env_path:
        p = Path(env_path)
        if p.is_file():
            us["lilypondPath"] = str(p.resolve())
            return
    if BUNDLED_LILYPOND.is_file():
        us["lilypondPath"] = str(BUNDLED_LILYPOND.resolve())


def process_musicxml_to_ly(input_path: Path, output_path: Path) -> None:
    """Load ``input_path``, run ``transform_score``, write ``output_path`` as ``.ly``."""
    _configure_lilypond_path()

    try:
        parsed = converter.parse(str(input_path))
    except Exception as exc:  # music21 raises various parse errors
        print(f"Error: could not parse {input_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    transform_score(parsed)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        parsed.write("lilypond", fp=str(output_path))
    except Exception as exc:
        if _LilyTranslateException is not None and isinstance(exc, _LilyTranslateException):
            print(
                f"Error: could not write LilyPond ({output_path}): {exc}\n"
                "Install LilyPond and/or set the LILYPOND_PATH environment variable to "
                f"``lilypond`` (checked bundled: {BUNDLED_LILYPOND}).",
                file=sys.stderr,
            )
        else:
            print(f"Error: could not write {output_path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Wrote {output_path}")
