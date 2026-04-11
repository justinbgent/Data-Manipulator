"""In-place score edits applied after parse and before write."""

from __future__ import annotations

from music21 import chord, note, pitch, stream

from pitch_map import MIDI_TO_TARGET_NAME


def _rewrite_pitch(p: pitch.Pitch) -> pitch.Pitch | None:
    name = MIDI_TO_TARGET_NAME.get(p.midi)
    if name is None:
        return None
    return pitch.Pitch(name)


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
