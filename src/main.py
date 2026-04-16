"""Read MusicXML, rewrite pitches, write MusicXML.

Run from ``src`` (so imports resolve)::

    cd src
    python main.py -i .                         --- Converts all files in input directory
    python main.py -i . -o my_outputs           --- Batch output under src/output/my_outputs/
    python main.py -i piece.musicxml            --- Converts single file
    python main.py -i piece.musicxml -o out.xml --- Single file to chosen path

``-i`` may be a file or a directory (use ``.`` for ``src/input``). Batch mode writes
``<stem>_out.musicxml`` per file. No LilyPond is required.

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
# python main.py -i . -o my_batch_outputs
