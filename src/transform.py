"""In-place score edits applied after parse and before write."""

from __future__ import annotations

from music21 import chord, note, pitch, stream

from pitch_map import PS_TO_TARGET_PS


def _rewrite_pitch(p: pitch.Pitch) -> pitch.Pitch | None:
    if not p.isTwelveTone():
        return None
    target_ps = PS_TO_TARGET_PS.get(int(round(p.ps)))
    if target_ps is None:
        return None
    out = pitch.Pitch()
    out.ps = float(target_ps)
    return out


def transform_score(score: stream.Stream) -> None:
    """Rewrite notated pitches to the piano-style spelling table (see ``pitch_map``)."""
    for elem in score.recurse():
        if isinstance(elem, chord.Chord):
            new_pitches: list[pitch.Pitch] = []
            changed = False
            for p in elem.pitches:
                np = _rewrite_pitch(p)
                if np is not None:
                    new_pitches.append(np)
                    changed = True
                else:
                    new_pitches.append(p)
            if changed:
                elem.pitches = new_pitches
        elif isinstance(elem, note.Note) and not elem.isRest:
            np = _rewrite_pitch(elem.pitch)
            if np is not None:
                elem.pitch = np
