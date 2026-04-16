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
    # Top key of 88 key piano   # Note line positions (relative to treble going up, and bass going down):
    ("C8", ("C", 11)),          # 43
    # Clef 3 (+3 octaves)
    ("B7", ("B", 10)),          # 42
    ("A#7", ("A", 10)),         # 41
    ("A7", ("G", 10)),          # 40
    ("G#7", ("F", 10)),         # 39
    ("G7", ("E", 10)),          # 38
    ("F#7", ("D", 10)),         # 37
    ("F7", ("C", 10)),          # 36        # -6 - 36 = -42
    ("E7", ("B", 9)),           # 35
    ("D#7", ("A", 9)),          # 34
    ("D7", ("G", 9)),           # 33
    ("C#7", ("F", 9)),          # 32
    ("C7", ("E", 9)),           # 31
    # Clef 2 (+2 octaves)
    ("B6", ("D", 9)),           # 30
    ("A#6", ("C", 9)),          # 29
    ("A6", ("B", 8)),           # 28
    ("G#6", ("A", 8)),          # 27
    ("G6", ("G", 8)),           # 26
    ("F#6", ("F", 8)),          # 25
    ("F6", ("E", 8)),           # 24        # -6 - 24 = -30
    ("E6", ("D", 8)),           # 23
    ("D#6", ("C", 8)),          # 22
    ("D6", ("B", 7)),           # 21
    ("C#6", ("A", 7)),          # 20
    ("C6", ("G", 7)),           # 19
    # Clef 1 (+1 octave)
    ("B5", ("F", 7)),           # 18
    ("A#5", ("E", 7)),          # 17
    ("A5", ("D", 7)),           # 16
    ("G#5", ("C", 7)),          # 15
    ("G5", ("B", 6)),           # 14
    ("F#5", ("A", 6)),          # 13
    ("F5", ("G", 6)),           # 12        # -6 - 12 = -18
    ("E5", ("F", 6)),           # 11
    ("D#5", ("E", 6)),          # 10
    ("D5", ("D", 6)),           # 9
    ("C#5", ("C", 6)),          # 8
    ("C5", ("B", 5)),           # 7
    # Clef 0 (created with treble in LilyPond)
    ("B4", ("A", 5)),           # 6
    ("A#4", ("G", 5)),          # 5
    ("A4", ("F", 5)),           # 4
    ("G#4", ("E", 5)),          # 3
    ("G4", ("D", 5)),           # 2
    ("F#4", ("C", 5)),          # 1
    ("F4", ("B", 4)),           # 0         # -6 - 0 = -6 (Mid-C line position)
    ("E4", ("A", 4)),           # -1
    ("D#4", ("G", 4)),          # -2
    ("D4", ("F", 4)),           # -3
    ("C#4", ("E", 4)),          # -4
    ("C4", ("D", 4)),           # -5
    # Cleff -1
    ("B3", ("C", 4)),           # -6 / 6
    ("A#3", ("B", 3)),          # 5
    ("A3", ("A", 3)),           # 4
    ("G#3", ("G", 3)),          # 3
    ("G3", ("F", 3)),           # 2
    ("F#3", ("E", 3)),          # 1
    ("F3", ("D", 3)),           # 0         # 6 - 0 = 6
    ("E3", ("C", 3)),           # -1
    ("D#3", ("B", 2)),          # -2
    ("D3", ("A", 2)),           # -3
    ("C#3", ("G", 2)),          # -4
    ("C3", ("F", 2)),           # -5
    # Cleff -2
    ("B2", ("E", 2)),           # -6
    ("A#2", ("D", 2)),          # -7
    ("A2", ("C", 2)),           # -8
    ("G#2", ("B", 1)),          # -9
    ("G2", ("A", 1)),           # -10
    ("F#2", ("G", 1)),          # -11
    ("F2", ("F", 1)),           # -12       # 6 - -12 = 18
    ("E2", ("E", 1)),           # -13
    ("D#2", ("D", 1)),          # -14
    ("D2", ("C", 1)),           # -15
    ("C#2", ("B", 0)),          # -16
    ("C2", ("A", 0)),           # -17
    # Clef -3
    ("B1", ("G", 0)),           # -18
    ("A#1", ("F", 0)),          # -19
    ("A1", ("E", 0)),           # -20
    ("G#1", ("D", 0)),          # -21
    ("G1", ("C", 0)),           # -22
    ("F#1", ("B", -1)),         # -23
    ("F1", ("A", -1)),          # -24       # 6 - -24 = 30
    ("E1", ("G", -1)),          # -25
    ("D#1", ("F", -1)),         # -26
    ("D1", ("E", -1)),          # -27
    ("C#1", ("D", -1)),         # -28
    ("C1", ("C", -1)),          # -29
    # Bottom 3 piano keys of 88
    ("B0", ("B", -2)),          # -30
    ("A#0", ("A", -2)),         # -31
    ("A0", ("G", -2)),          # -32
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
