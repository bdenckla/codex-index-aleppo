"""Exports main

TWO ROOTS, AND HERE THEY HAPPEN TO BE ONE DIRECTORY.  ``_DATA_ROOT`` below is the
DATA this pipeline reads and writes -- the hand-made CSV of J David Stark's Aleppo
Codex index, and the three artifacts derived from it -- and it is spelled off
``__file__`` because that data currently sits in the same directory as the code
that makes it.  Phase 1 of
``MAM-basics/doc/PLAN-evacuate-python-from-codex-index-trio.md`` names the two apart
anyway: at Phase 3 the Python leaves for MAM-basics and the four files stay here, so
``_DATA_ROOT`` becomes a sibling-repo path and nothing else in this pipeline changes.

WHY THE FOUR PATHS WERE DEAD, WHICH IS WHY THIS FILE IS THE FIRST THING PHASE 1
TOUCHED.  They were the cwd-relative literals ``"aleppo/..."`` until 2026-08-22,
naming the directory this tree had before ``9025037`` (2026-03-28) renamed
``codex-index/aleppo`` to ``codex-index-aleppo/aleppo-wiki`` -- see ``provenance.md``
beside this file.  The rename did not repoint them, so from that day the generator
raised ``FileNotFoundError`` from every working directory, and its three outputs had
no producer at all for five months.
"""

from pathlib import Path

from py.read_csv_file import read_csv_file
from py.group_by_book import group_by_book
from py.write_wikitext_file import write_wikitext_file


def main():
    data_entries = read_csv_file(_CSV_IN_PATH, _JSON_OUT_PATH_1)
    grouped = group_by_book(data_entries, _JSON_OUT_PATH_2)
    write_wikitext_file(grouped, _WIKITEXT_OUT_PATH)


_DATA_ROOT = Path(__file__).resolve().parent
_CSV_IN_PATH = _DATA_ROOT / "J David Stark Aleppo Codex Index.csv"
_JSON_OUT_PATH_1 = _DATA_ROOT / "index-flat.json"
_JSON_OUT_PATH_2 = _DATA_ROOT / "index-grouped-by-book.json"
_WIKITEXT_OUT_PATH = _DATA_ROOT / "index.wiki"


if __name__ == "__main__":
    main()
