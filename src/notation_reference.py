"""Personal reference: staff layout, MusicXML pitch, and Lily Pond line positions.

The CLI uses music21 to transform notes and write MusicXML; you can convert that to LilyPond/PDF
elsewhere (e.g. ``musicxml2ly``) if needed.

Runtime pitch pairs live in ``pitch_map`` (one spelling per chromatic height; enharmonics
match via ``round(Pitch.ps)``). Open this module when you need the staff commentary.

Relative ``-i`` paths are read from ``src\\input\\``. Relative ``-o`` paths are written under
``src\\output\\``. Use absolute paths for ``-i`` or ``-o`` to read/write anywhere else.
Default output if ``-o`` omitted: ``src\\output\\<input_stem>_out.musicxml``.
Rewrites are defined in ``pitch_map`` / ``transform.transform_score``.

How the program works:

1. ``-i``/``--input``: MusicXML file (.xml, .musicxml, or .mxl); relative names use ``src\\input\\``.
2. music21 ``converter.parse()`` loads the file into a stream (Score, Part, etc.).
3. ``transform_score()`` rewrites pitches in place using ``pitch_map`` (add more logic there if needed).
4. The stream is written with ``write("musicxml", fp=...)`` to a ``.musicxml`` (or ``.xml``) file.
5. ``-o``/``--output`` is optional; relative paths go under ``src\\output\\``; default output name
   is ``<input_stem>_out.musicxml`` in ``src\\output\\`` (or a batch output directory).
   If the output directory does not exist, it is created. Parse/write errors go to stderr
   and the program exits with status 1.

MusicXML pitch element::

    <pitch>
      <step>C</step>
      <octave>4</octave>
      <alter>0</alter>
    </pitch>

C on 4th octave is middle C.
alter values are -1, 0, 1 for -1 half step, 0 no change, 1 half step.
Or in other words, -1 is a flat, 0 is a natural, 1 is a sharp.

Staff continuing above treble (+2 octaves; left same chromatic descent; right: C6 to G7, C#6 to A7, then each step up the left adds the next natural — G7..D9 opposite C6..B6):

B6 to D9,
A#6 to C9,
A6 to B8,
G#6 to A8,
G6 to G8,
F#6 to F8,
F6 to E8,
E6 to D8,
D#6 to C8,
D6 to B7,
C#6 to A7,
C6 to G7,

Staff continuing immediately above treble (left: +1 octave).
B5 to F7,
A#5 to E7,
A5 to D7,
G#5 to C7,
G5 to B6,
F#5 to A6,
F5 to G6,
E5 to F6,
D#5 to E6,
D5 to D6,
C#5 to C6,
C5 to B5,

*** Treble from top to bottom: ***********************
B4 to A5,
A#4 to G5,
A4 to F5,
G#4 to E5,
G4 to D5,
F#4 to C5,
F4 to B4,
E4 to A4,
D#4 to G4,
D4 to F4,
C#4 to E4,
C4 to D4,
******************************************************

Bass from top to bottom:
B3 to C4
A#3 to B3
A3 to A3
G#3 to G3
G3 to F3
F#3 to E3
F3 to D3
E3 to C3
D#3 to B2
D3 to A2
C#3 to G2
C3 to F2

Staff continuing immediately below bass clef (left: same descent as bass, octave lower; right: naturals only, E2 down white keys):
B2 to E2,
A#2 to D2,
A2 to C2,
G#2 to B1,
G2 to A1,
F#2 to G1,
F2 to F1,
E2 to E1,
D#2 to D1,
D2 to C1,
C#2 to B0,
C2 to A0,

Note what I am describe visually will look like how the piano is layed out. Black lines for
sharps/flats, white spaces for naturals. The goal is to make it more intuitive for which
key to press.

Staff line positions:
Sharps/Flats will fall on staff lines, naturals will fall in white spaces between lines.
In Lily Pond, the treble clef lines will be -4, -2, 1, 3, 5.
Lines not shown, white spaces are naturals: -5(C4), -3(D4), -1(E4), 0(F4), 2(G4), 4(A4), 6(B4)
This pattern will repeat for each octave. And now sharps and flats have dedicated positions.
"""
