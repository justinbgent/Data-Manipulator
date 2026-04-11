"""Pitch rewrite table from ``notation_reference`` (staff ↔ piano-style spelling).

Each pair is ``(source_pitch_string, target_spelling)`` as music21 pitch strings.
Sources are one spelling per chromatic height; any enharmonic shares the same
``round(pitch.ps)`` and therefore matches without listing equivalents.
"""

from __future__ import annotations

from music21 import pitch

# (from, to) — order matches notation_reference.py comments.
_PITCH_PAIRS: list[tuple[str, str]] = [
    # Staff continuing above treble (+2 octaves)
    ("B6", "D9"),
    ("A#6", "C9"),
    ("A6", "B8"),
    ("G#6", "A8"),
    ("G6", "G8"),
    ("F#6", "F8"),
    ("F6", "E8"),
    ("E6", "D8"),
    ("D#6", "C8"),
    ("D6", "B7"),
    ("C#6", "A7"),
    ("C6", "G7"),
    # Immediately above treble (+1 octave on the left)
    ("B5", "F7"),
    ("A#5", "E7"),
    ("A5", "D7"),
    ("G#5", "C7"),
    ("G5", "B6"),
    ("F#5", "A6"),
    ("F5", "G6"),
    ("E5", "F6"),
    ("D#5", "E6"),
    ("D5", "D6"),
    ("C#5", "C6"),
    ("C5", "B5"),
    # Treble clef
    ("B4", "A5"),
    ("A#4", "G5"),
    ("A4", "F5"),
    ("G#4", "E5"),
    ("G4", "D5"),
    ("F#4", "C5"),
    ("F4", "B4"),
    ("E4", "A4"),
    ("D#4", "G4"),
    ("D4", "F4"),
    ("C#4", "E4"),
    ("C4", "D4"),
    # Bass clef
    ("B3", "C4"),
    ("A#3", "B3"),
    ("A3", "A3"),
    ("G#3", "G3"),
    ("G3", "F3"),
    ("F#3", "E3"),
    ("F3", "D3"),
    ("E3", "C3"),
    ("D#3", "B2"),
    ("D3", "A2"),
    ("C#3", "G2"),
    ("C3", "F2"),
    # Immediately below bass
    ("B2", "E2"),
    ("A#2", "D2"),
    ("A2", "C2"),
    ("G#2", "B1"),
    ("G2", "A1"),
    ("F#2", "G1"),
    ("F2", "F1"),
    ("E2", "E1"),
    ("D#2", "D1"),
    ("D2", "C1"),
    ("C#2", "B0"),
    ("C2", "A0"),
]


def build_ps_to_target_name() -> dict[int, str]:
    """Map twelve-tone pitch space (``round(Pitch.ps)``) to target ``nameWithOctave``."""
    out: dict[int, str] = {}
    for src, dst in _PITCH_PAIRS:
        ps_key = int(round(pitch.Pitch(src).ps))
        dst_name = pitch.Pitch(dst).nameWithOctave
        if ps_key in out and out[ps_key] != dst_name:
            msg = (
                f"Duplicate source ps {ps_key} for {src!r} "
                f"and existing {out[ps_key]!r} vs {dst_name!r}"
            )
            raise ValueError(msg)
        out[ps_key] = dst_name
    return out


PS_TO_TARGET_NAME: dict[int, str] = build_ps_to_target_name()
