"""Pitch rewrite table from ``notation_reference`` (staff ↔ piano-style spelling).

Each pair is ``(source_pitch_string, (target_step, target_octave))`` with
``target_step`` in ``A``–``G`` and ``target_octave`` as music21 octaves (including
negative values). Building with ``Pitch(step=..., octave=...)`` avoids ambiguous
strings such as ``"B-1"``, which parses as B-flat in octave 1, not B-natural in
octave ``-1``.

Sources are one spelling per chromatic height; any enharmonic shares the same
``round(pitch.ps)`` and therefore matches without listing equivalents.
``PS_TO_TARGET_PS`` maps source ``ps`` to target ``ps`` (both rounded to integers).
"""

from __future__ import annotations

from music21 import pitch

# (from, (step, octave)) — order matches notation_reference.py comments.
_PITCH_PAIRS: list[tuple[str, tuple[str, int]]] = [
    # Top key of 88 key piano
    ("C8", ("C", 11)),
    # Clef 3 (+3 octaves)
    ("B7", ("B", 10)),
    ("A#7", ("A", 10)),
    ("A7", ("G", 10)),
    ("G#7", ("F", 10)),
    ("G7", ("E", 10)),
    ("F#7", ("D", 10)),
    ("F7", ("C", 10)),
    ("E7", ("B", 9)),
    ("D#7", ("A", 9)),
    ("D7", ("G", 9)),
    ("C#7", ("F", 9)),
    ("C7", ("E", 9)),
    # Clef 2 (+2 octaves)
    ("B6", ("D", 9)),
    ("A#6", ("C", 9)),
    ("A6", ("B", 8)),
    ("G#6", ("A", 8)),
    ("G6", ("G", 8)),
    ("F#6", ("F", 8)),
    ("F6", ("E", 8)),
    ("E6", ("D", 8)),
    ("D#6", ("C", 8)),
    ("D6", ("B", 7)),
    ("C#6", ("A", 7)),
    ("C6", ("G", 7)),
    # Clef 1 (+1 octave)
    ("B5", ("F", 7)),
    ("A#5", ("E", 7)),
    ("A5", ("D", 7)),
    ("G#5", ("C", 7)),
    ("G5", ("B", 6)),
    ("F#5", ("A", 6)),
    ("F5", ("G", 6)),
    ("E5", ("F", 6)),
    ("D#5", ("E", 6)),
    ("D5", ("D", 6)),
    ("C#5", ("C", 6)),
    ("C5", ("B", 5)),
    # Clef 0 (created with treble in LilyPond)
    ("B4", ("A", 5)),
    ("A#4", ("G", 5)),
    ("A4", ("F", 5)),
    ("G#4", ("E", 5)),
    ("G4", ("D", 5)),
    ("F#4", ("C", 5)),
    ("F4", ("B", 4)),
    ("E4", ("A", 4)),
    ("D#4", ("G", 4)),
    ("D4", ("F", 4)),
    ("C#4", ("E", 4)),
    ("C4", ("D", 4)),
    # Cleff -1
    ("B3", ("C", 4)),
    ("A#3", ("B", 3)),
    ("A3", ("A", 3)),
    ("G#3", ("G", 3)),
    ("G3", ("F", 3)),
    ("F#3", ("E", 3)),
    ("F3", ("D", 3)),
    ("E3", ("C", 3)),
    ("D#3", ("B", 2)),
    ("D3", ("A", 2)),
    ("C#3", ("G", 2)),
    ("C3", ("F", 2)),
    # Cleff -2
    ("B2", ("E", 2)),
    ("A#2", ("D", 2)),
    ("A2", ("C", 2)),
    ("G#2", ("B", 1)),
    ("G2", ("A", 1)),
    ("F#2", ("G", 1)),
    ("F2", ("F", 1)),
    ("E2", ("E", 1)),
    ("D#2", ("D", 1)),
    ("D2", ("C", 1)),
    ("C#2", ("B", 0)),
    ("C2", ("A", 0)),
    # Clef -3
    ("B1", ("G", 0)),
    ("A#1", ("F", 0)),
    ("A1", ("E", 0)),
    ("G#1", ("D", 0)),
    ("G1", ("C", 0)),
    ("F#1", ("B", -1)),
    ("F1", ("A", -1)),
    ("E1", ("G", -1)),
    ("D#1", ("F", -1)),
    ("D1", ("E", -1)),
    ("C#1", ("D", -1)),
    ("C1", ("C", -1)),
    # Bottom 3 piano keys of 88
    ("B0", ("B", -2)),
    ("A#0", ("A", -2)),
    ("A0", ("G", -2)),
]


def build_ps_to_target_ps() -> dict[int, int]:
    """Map twelve-tone pitch space (``round(Pitch.ps)``) to target ``round(Pitch.ps)``."""
    out: dict[int, int] = {}
    for src, (dst_step, dst_octave) in _PITCH_PAIRS:
        ps_key = int(round(pitch.Pitch(src).ps))
        dst_p = pitch.Pitch(step=dst_step, octave=dst_octave)
        ps_val = int(round(dst_p.ps))
        out[ps_key] = ps_val
    return out


PS_TO_TARGET_PS: dict[int, int] = build_ps_to_target_ps()
