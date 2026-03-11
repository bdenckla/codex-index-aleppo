# CLAUDE.md — Project notes for AI assistants

## Verse numbering

**Always use MAM-standard verse numbering.** Never rely on your own notion of
the Masoretic text or its verse numbering.

If you suspect a verse-numbering discrepancy (e.g. between the docs and the
index), look up the BHS verse numbering via:

    C:\Users\BenDe\GitRepos\MAM-simple\out\json-vtrad-bhs\<Book>.json

Each entry there has an `"osisID-of-MAM-src"` field that maps the BHS osisID
to the MAM source verse.  Use this as the authoritative cross-reference.

Example: BHS `Jer.31.35` has `"osisID-of-MAM-src": "Jer.31.34"`, meaning
what MAM calls Jer 31:34 is what BHS calls Jer 31:35.
