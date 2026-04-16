"""Read MusicXML, rewrite pitches, write LilyPond ``.ly`` files.

Run from ``src`` (so imports resolve)::

    cd src
    python main.py -i .                         --- Converts all files in input directory
    python main.py -i . -o my_lys               --- Converts all files in input directory to my_lys directory
    python main.py -i piece.musicxml            --- Converts single file
    python main.py -i piece.musicxml -o my_ly   --- Converts single file to my_ly file

``-i`` may be a file or a directory (use ``.`` for ``src/input``). Batch mode writes
``<stem>_out.ly`` per file. music21 needs a ``lilypond`` executable for export: set
``LILYPOND_PATH`` or place LilyPond at ``../lilypond-2.24.4/bin/lilypond.exe``.

See ``paths``, ``cli``, ``pitch_map``, ``transform``; staff commentary in ``notation_reference``.
"""

from __future__ import annotations

from cli import main

if __name__ == "__main__":
    main()

# How to convert:
# cd src
# python main.py -i .
# python main.py -i piece.musicxml
# python main.py -i . -o my_batch_lys