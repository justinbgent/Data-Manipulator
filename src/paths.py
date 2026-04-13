"""Input/output roots and path resolution for the CLI.

Relative ``-i`` is under ``src/input/``; relative ``-o`` (or default) is under
``src/output/`` (``<stem>_out.ly``). Absolute ``-i``/``-o`` use those paths.
"""

from __future__ import annotations

from pathlib import Path

_SRC_DIR = Path(__file__).resolve().parent
REPO_ROOT = _SRC_DIR.parent
INPUT_DIR = _SRC_DIR / "input"
OUTPUT_DIR = _SRC_DIR / "output"
BUNDLED_LILYPOND = REPO_ROOT / "lilypond-2.24.4" / "bin" / "lilypond.exe"

_MUSICXML_SUFFIXES = frozenset({".xml", ".musicxml", ".mxl"})


def resolve_input_path(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (INPUT_DIR / path).resolve()


def resolve_output_path(out_arg: Path | None, input_path: Path) -> Path:
    if out_arg is None:
        return (OUTPUT_DIR / f"{input_path.stem}_out.ly").resolve()
    out_arg = out_arg.expanduser()
    if out_arg.is_absolute():
        return out_arg.resolve()
    return (OUTPUT_DIR / out_arg).resolve()


def resolve_output_directory(out_arg: Path | None) -> Path:
    """Batch mode: all outputs go under this directory (created if missing)."""
    if out_arg is None:
        d = OUTPUT_DIR
    else:
        out_arg = out_arg.expanduser()
        d = out_arg if out_arg.is_absolute() else (OUTPUT_DIR / out_arg)
    d.mkdir(parents=True, exist_ok=True)
    return d.resolve()


def iter_musicxml_files(directory: Path) -> list[Path]:
    """Non-recursive list of MusicXML files in ``directory``."""
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in _MUSICXML_SUFFIXES
    )
