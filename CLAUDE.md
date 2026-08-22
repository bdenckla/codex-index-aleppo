# CLAUDE.md — Project notes for AI assistants

What this repo is, what it publishes, and what each data directory holds are in
[README.md](README.md).

## There is no Python here — the code is `../MAM-basics/py/`

Every `.py` this repo tracked left on 2026-08-22, under Phase 4 of
`../MAM-basics/doc/PLAN-evacuate-python-from-codex-index-trio.md`. **Fifty files: do not put
one back.** They emptied `py/`, `py/tests/`, `py/py_ac_loc/`, `py/py_ac_word_image_helper/`,
`py/mb_cmn/` and `aleppo-wiki/py/` outright.

**Twenty-one of the fifty did not move — they were deleted as duplicates**, MAM-basics already
holding the same text:

- `py/py_ac_word_image_helper/` (6) — one committed blob with MAM-basics' copy, which arrived
  with book-of-job's own evacuation on 2026-08-19.
- `py/mb_cmn/` (4) — vendored from MAM-basics, byte-identical.
- Six of `aleppo-wiki/py/` — `hebrew_letters`, `hebrew_punctuation`, `hebrew_verse_numerals`
  and `my_utils` under their own names, plus two renamed: `mam_book_names` is MAM-basics'
  `mb_cmn/mam_bknas`, and `my_open` is its `mb_cmn/file_io`.
- `py/check_mark_order.py`, `check_escape_sequences.py`, `fix_mark_order.py` and
  `fix_escape_sequences.py` — MAM-basics holds all four. What they needed was this repo's data
  brought into their scope, not a second copy of the script.
- `py/tests/test_h_dot_below_nfc.py` — folded into MAM-basics' copy as a scope of its own.

**The naming rule for the twenty-nine that did move is mechanical: `main_ac_` or `check_ac_`
plus the module's own name.** It was applied to all fifteen top-level modules, not only the
five whose names were already taken, because codex-index-cam1753 holds a counterpart of six of
them against the same problem on a different manuscript. `py/py_ac_loc/` kept its name;
`aleppo-wiki/py/` became `py/ac_wiki/`.

**One file moved with this code without belonging to it.** `py/gen_permission_glob.py` turns a
shell command into a Claude Code permission glob and mentions no manuscript, no codex and no
Hebrew. It landed as MAM-basics' `py/main_gen_permission_glob.py`, unprefixed.

**`requirements.txt` went with the Python, on Ben's decision of 2026-08-22.** It named black,
matplotlib and pyspellchecker, and nothing here imports any of them now.
`.github/workflows/pages.yml` was checked rather than assumed and runs no Python at all, so the
Pages deploy this repo keeps was never a reason to hold the file. The declaration had also been
wrong in both directions since long before the move: it omitted Pillow and numpy, without which
the code could not run, and named a pyspellchecker neither codex-index repo has ever imported.
**What the moved code needs is declared in MAM-basics' own `requirements.txt` now.**

**`codex-index-aleppo.code-workspace` went the same day and on the same decision.** Half of it
was dead outright — a `chat.tools.terminal.autoApprove` block naming `.venv\Scripts\python.exe`.
The other half was never about Python: the file declared a three-folder view opening this repo
beside book-of-job and codex-index-cam1753. **book-of-job's workspace file declared that same
cluster and was deleted on 2026-08-21, and codex-index-cam1753's went with its own Phase 4**, so
nothing opens those three repos together any more. MAM-basics' `all-repos.code-workspace` still
lists this repo, and is where a sweep of Ben's repos reaches it.

**`.claude/settings.json` went too, and NOT because the move orphaned it.** Six of its ten
permission globs were still live — `Bash(git *)`, three `gh issue` globs, a `Read()` over the
Yeivin *Introduction to the Tiberian Masorah* scans, and one that still matched when a session
sitting here reached sideways for MAM-basics' interpreter. **Ben's reason, 2026-08-22, is that
the file predates Claude Code's "auto" permission mode**, and dates from a period of trying hard
and with little success to get permission globs set up at all. So it is a fossil of an approach
he has moved off rather than a casualty of the evacuation. **Do not write a new one**: this repo
was the only one of the three that had a `.claude/` at all, and the directory is gone with it.

## What MAM-basics writes here, and what it reads

Run any of these from anywhere; each addresses this repo by absolute path, through
`MAM-basics/py/ac_paths.py`.

**The Wikisource index — three files under `aleppo-wiki/`.** `index-flat.json`,
`index-grouped-by-book.json` and `index.wiki`, from the hand-made
`aleppo-wiki/J David Stark Aleppo Codex Index.csv`:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_ac_wikisource_page.py
```

That was `aleppo-wiki/main_make_wikisource_page.py` here until the move. The name changed
because codex-index-leningrad has a file of that name too, and the two are different tools
against different input formats.

**The annotated flat index — `index-flat-annotated.json` at this repo's root**, from
`aleppo-wiki/index-flat-corrected.json`:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_ac_gen_index_flat_annotated.py
```

**Regenerating those four is how a change is verified**: all four come back byte-identical
unless something real has changed, which is what MAM-basics' Phase 3 used as its oracle.
Compare against `git cat-file blob HEAD:<path>`, **not** with `git status --porcelain` — see
the warning below.

**Four more entry points read this repo's data and write only into `.novc/` or the browser**:
`main_ac_gen_flat_stream.py`, `main_ac_gen_line_break_editor.py`,
`main_ac_gen_col_quad_editor.py` and `main_ac_merge_line_markers.py`. The line-break and
column-coordinate workflows are human-in-the-loop: the editor produces a browser download that
a human moves into `line-breaks/` or `column-coordinates/`. See
[`doc/aleppo-line-breaks.md`](doc/aleppo-line-breaks.md).

## `git status --porcelain` lies about this repo, in both directions

**152 of this repo's 222 tracked files were CRLF on disk against an LF blob** when that was
measured on 2026-08-22, `.gitattributes` declaring `* text=auto eol=lf` throughout. A
regeneration that writes LF then changes the file's size, and git flags the size change before
re-hashing settles it — so `git status` reported four freshly regenerated artifacts as modified
while `git diff` was empty. It has also gone wrong the other way, calling a tree clean while a
tracked file sat CRLF.

**Compare bytes against the blob instead**, which is immune to it:

```powershell
git cat-file blob HEAD:aleppo-wiki/index.wiki
```

## What `check_ac_all.py` reports, and why two of its four fail

Neither failure was caused by the evacuation, and MAM-basics reproduces the word-finding one at
exactly its old tally, which is the evidence that the move changed no behaviour.

- **`check_ac_word_finding.py` fails 160 of 160.** It compares a column identifier against an
  integer — `col: found=1of2 expected=1`. This repo's line-break JSON has moved to an N-of-M
  column identifier (`"col": "1of3"`) since `eb4bcaf` on 2026-03-14, and the check has not been
  touched since. **Every one of the 160 failures is a `col:` clause and not one is a `line:` or
  a `word:` clause**, so the located positions are right in all 160 cases.
  codex-index-cam1753 keeps `"col": 1` and its structurally identical check passes.
- **`check_line_breaks` reports 93 issues over all 35 pages**, and until 2026-08-22 it did not
  report at all: it raised `ValueError: Unhandled tag <spi-invnun> in verse Ps.107.23` before
  writing anything, so `check_line_breaks.html` was a fossil of a run that had only ever seen
  page 270r. MAM-basics' `b37bdb4` taught the MAM-XML reader to skip the inverted nun — the
  seven of Psalm 107 — and `a50f40e` here is the first complete report.

**70 of those 93 issues are one cause, and it is the cause of the 160 above.** "No col 1 line
markers; No col 2 line markers" appears on 29 of the 35 pages because the check asks for `col 1`
and `col 2` where the data now says `1of3` and `2of3`. **Fixing the N-of-M migration would close
both failures at once.** The remaining six pages carry the genuinely new signal: columns short of
28 lines with gaps in the numbering, an unhandled `blank-line` item type, one word after the last
line-end, and on page 004r a five-word alignment mismatch against `MAM-XML/`, each offset by a
single word.

## Viewing a word in Aleppo Codex images

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_ac_find_word_in_images.py Job 3:17 "יָ֝נ֗וּחוּ"
```

Arguments are `<book> <c:v> "<word>"`. The script looks up the word in `line-breaks/`, crops the
page image from `aleppo-pages/` around it with a fade overlay, generates an HTML preview in
`.novc/` and opens it in the browser. Use `--wide` for a wider crop. Where line-break data is
not available for the book, it falls back to `index-flat-annotated.json` and reports the page ID
only.

That was `py/main_find_word_in_aleppo_images.py` here. Besides being renamed, it was repaired on
the way: it used to replace `sys.stdout` at import time, which discarded whatever the previous
stream had buffered and so silently swallowed output a caller had already printed.

## Verse numbering

**Always use MAM-standard verse numbering.** Never rely on your own notion of the Masoretic text
or its verse numbering.

If you suspect a verse-numbering discrepancy, look up BHS verse numbering via
`../MAM-simple/out/json-vtrad-bhs/<Book>.json`. Each entry has an `"osisID-of-MAM-src"` field
mapping BHS osisID to MAM source verse. Example: BHS `Jer.31.35` → `"osisID-of-MAM-src":
"Jer.31.34"`.

## Hebrew Unicode mark order — no NFC normalization

**Never apply Unicode normalization (NFC, NFD, etc.) to Hebrew text here.** NFC reorders
combining marks, destroying the mark order this data is written in. If strings that should be
equal are not matching, put both through the project's standard mark order — do not paper over it
with `unicodedata.normalize`.

The order is specified and implemented in `../MAM-basics/py/mb_cmn/uni_denorm.py`
(`give_std_mark_order` is the authority, `has_std_mark_order` the predicate), and
`../MAM-basics/py/check_mark_order.py` is the checker. Both moved there with the rest of the
code; the rule they enforce is unchanged.

## MAM-basics still lints this repo, and still scans it for NFC

Deleting the code here did not end the checks that ran over this repo's data.

- **`py/tests/test_h_dot_below_nfc.py` here was deleted**, but MAM-basics' own copy carries a
  `codex-index-aleppo` scope that walks this repo's tracked files. **26 files are in scope after
  the move**, measured 2026-08-22, the artifact trees and the two binary precursors being
  excluded.
- **`check_mark_order.py` and `check_escape_sequences.py` in MAM-basics take a union of
  per-repo scope lists**, and `ac_paths.code_paths()` plus this repo's data root are two entries
  in it. So this repo's 78 hand-made line-break, column-coordinate and flat-stream JSON are
  still read for mark order.

A decomposed h-with-dot-below or a stray `\uXXXX` escape authored here is therefore still
caught — by a run of MAM-basics' suite and `py/check_all.py`, not by anything here.

## What no program writes

**154 of this repo's 162 tracked artifacts are written by no program**, and will not come back
if they are lost. Only eight are generated: the three under `aleppo-wiki/`,
`index-flat-annotated.json`, `check_line_breaks.html` and the three PNGs under
`plot_col_coords-out/`.

| Tree | Files | Where it comes from |
|---|---|---|
| `aleppo-pages/` | 37 | downloaded scans from archive.org |
| `line-breaks/` | 35 | human-annotated, through the editor |
| `column-coordinates/` | 35 | human-annotated, through the editor |
| `MAM-XML/` | 24 | vendored snapshot of MAM-simple's `xml-vtrad-mam` |
| `aleppo-wiki/` | 10 | the CSV index, its five precursors, `index-flat-corrected.json`, three Wikisource notes |
| `ds-flat-stream/` | 8 | generated, but see below |
| `gh-pages/` | 4 | hand-authored |
| `test-data-from-book-of-job.json` | 1 | hand-made |

**`ds-flat-stream/` is the one that looks regenerable and is not.** The generator takes explicit
per-page verse ranges as arguments, and those arguments are recorded nowhere — so the eight files
cannot be reproduced from anything tracked. Treat them as hand-made.

`aleppo-wiki/LICENSE.txt` and `aleppo-wiki/provenance.md` are the tree's own paperwork rather
than artifacts, which is why `aleppo-wiki/` counts 10 here against 15 tracked files.

## Minimum font size for pointed Hebrew

Never use smaller than **20pt** for pointed Hebrew in HTML. This applies to the hand-authored
pages under `gh-pages/` and to anything MAM-basics generates into this repo.

## Terminology: "Varika"

**Varika** = **U+FB1E HEBREW POINT JUDEO-SPANISH VARIKA** (Alphabetic Presentation Forms block),
not U+05BF HEBREW POINT RAFE (main Hebrew block).

## Do not mention private repos in public repos

This repo is public. Some sibling repos are private. Never reference a private repo by name in
commits, code, docs, or issue/PR text destined for a public repo.

## Detailed reference files

These were `.github/copilot-instructions-*.md` until 2026-08-03, when GitHub Copilot stopped
being used here. All four had every `py/…` path repointed on 2026-08-22 with the move.

- **[`doc/reading-mam-simple.md`](doc/reading-mam-simple.md)** — the vendored `MAM-XML/`
  snapshot and the reader over it; points at MAM-simple for the format itself
- **[`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md)** — MAM with Doc URLs and book codes
- **[`doc/aleppo-line-breaks.md`](doc/aleppo-line-breaks.md)** — line-break workflow, page image
  sources, Job leaf table
- **[`doc/ocr-with-kraken.md`](doc/ocr-with-kraken.md)** — Kraken OCR setup and usage. **Its two
  commands cannot be run on this machine**: kraken is in no venv here, and never was.
