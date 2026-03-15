# CLAUDE.md — Project notes for AI assistants

## Verse numbering

**Always use MAM-standard verse numbering.** Never rely on your own notion of the Masoretic text or its verse numbering.

If you suspect a verse-numbering discrepancy, look up BHS verse numbering via `../MAM-simple/out/json-vtrad-bhs/<Book>.json`. Each entry has an `"osisID-of-MAM-src"` field mapping BHS osisID to MAM source verse. Example: BHS `Jer.31.35` → `"osisID-of-MAM-src": "Jer.31.34"`.

## Python Environment — MANDATORY venv-qualified commands

Always use `.venv/` for Python work. **Never run bare `python`, `python3`, `pip`, or `pip3`** — always use the explicit venv path:

- **Windows:** `.venv\Scripts\python.exe` / `.venv\Scripts\pip.exe`
- **Linux/macOS:** `.venv/bin/python` / `.venv/bin/pip`

This rule applies everywhere — terminal, chat examples, documentation, tool invocations. No exceptions.

## No `python -c` — Use `.novc/` Scripts Instead

**Never use `python -c`** for any reason. Always write a temporary `.py` file in `./.novc/` (which is gitignored) and run it. Multi-line `-c` strings break Claude Code's permission glob matching and trigger approval prompts every time.

## No Multi-Line Shell Commands

**Never write a Bash command that spans multiple lines.** Claude Code's permission globs use `*` which does not match newlines — multi-line commands break glob matching and trigger approval prompts. When the payload is inherently multi-line, write it to a file and reference the file.

Common instances:
- **Git commit messages** — write to `.novc/commit_msg_<slug>.txt` with the Write tool, then `git commit -F .novc/commit_msg_<slug>.txt`
- **GitHub issue/PR bodies** — write to `.novc/issue_body.md`, then `gh issue create --body-file .novc/issue_body.md`
- **Python snippets** — write to `.novc/my_script.py`, then run with the venv Python

## Prefer Built-in Tools over Bash Equivalents

Default to Read, Write, Edit, Grep, Glob instead of Bash equivalents (`cat`, `echo >`, `sed`, `grep`, `find`). Every Bash command not pre-allowed triggers an approval prompt; built-in tools don't.

## UTF-8 Everywhere

On Windows, Python defaults to the system ANSI code page, not UTF-8 — this causes `charmap` errors with non-ASCII text. Fix this **in the code**, not with environment variable workarounds like `PYTHONUTF8=1` or `PYTHONIOENCODING=utf-8`.

1. Every `open()` call must include `encoding="utf-8"`.
2. `json.dump()` / `json.dumps()` must pass `ensure_ascii=False`.
3. `subprocess` output: pass `encoding="utf-8"`.
4. **stdout/stderr** — if a script must print non-ASCII, reconfigure the streams at the top of the script:
   ```python
   import sys, io
   sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
   sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
   ```
   Alternatively, write non-ASCII output to a file instead of stdout.
5. Never rely on the system default encoding.
6. **Never use `PYTHONUTF8=1`, `PYTHONIOENCODING`, or any env-var prefix** as a substitute for writing correct code.

## No Unsolicited Git Operations

Never run `git commit` or `git push` without explicit permission. Staging and status checks are fine.

## Never Amend Commits

Never use `git commit --amend` or `git rebase` unless explicitly asked. Always make new commits.

## Git Commit Messages — Use `-F`, Not Heredocs

Write commit messages to a **uniquely-named** file in `.novc/` with the Write tool, then commit with `-F`:

```bash
git commit -F .novc/commit_msg_<short_slug>.txt
```

Never reuse a fixed filename — a stale file silently produces the wrong message. Never write the file via Bash redirection; always use the Write tool. Never pre-check whether `.novc/` or the file exists — Write creates it unconditionally.

## Don't Redundantly Re-assert the Repo Directory

The working directory is already the project root. Run `git` directly without `cd` or `git -C <this-repo>`. For a sibling repo, use `git -C <path>`.

## Don't Close Issues Prematurely

Never close a GitHub issue until work is both committed **and** pushed. Closing before pushing leaves the issue marked resolved while the fix is only local.

## Before Discarding Work

Before any destructive git operation (`git reset`, `git checkout -- .`, `git stash drop`, etc.), run `git status` and `git diff --stat`. If there are uncommitted changes beyond the current experiment, alert the user first.

## Fail Fast — No Silent Error Smoothing

Do not write defensive code that swallows errors or returns `None` on unexpected conditions. Only catch exceptions when there is a concrete recovery strategy — never catch broad `Exception` or `KeyError` just to return `None`. These are batch pipelines; a crash with a clear traceback is the correct response to unexpected input.

## Dict Access Style

Be intentional about dict access:
- `d[key]` — when the key is **required** (a `KeyError` on a missing required key is a bug you want to hear about immediately)
- `d.get(key)` — when the key is **genuinely optional** and `None` is meaningful
- `d.get(key, default)` — when the key is optional and there is a natural default

## JSON Lists: Prepend, Don't Append

When adding to a semantically unordered JSON array, **prepend** rather than append. Appending requires a two-line diff (add comma to old last element + add new element); prepending is a clean one-line diff.

## Format Python with Black

After writing or editing any Python file, run black before committing:

```bash
.venv/Scripts/python.exe -m black <file_or_directory>
```

Format only files you changed. This is mandatory — not optional.

## Editing Python with Concrete Syntax Trees

For complex or numerous edits to Python files, consider [libcst](https://libcst.readthedocs.io/) to programmatically transform code rather than fragile text replacements. Especially useful for refactors that rename symbols or restructure imports.

## Global Variables

Avoid the `global` keyword and mutating module-level variables. Pass shared state as parameters or return it. Module-level constants (ALL_CAPS) are fine if immutable after definition.

## Python Package `__init__.py` Style

Keep `__init__.py` files minimal — package markers only. Do not add re-exports; always import directly from the submodule that defines the symbol.

## Script Promotion Policy

When a `.novc/` script becomes part of an ongoing, repeatable workflow, promote it to a permanent location (e.g. `py/py_ac_loc/`) immediately. Suggest promotion as soon as the pattern becomes clear.

## Opening HTML Files

- **Interactive editors** using `navigator.clipboard`, `canvas.toBlob()`, or cross-origin image access — serve over HTTP (`http://127.0.0.1`). Use a `serve_and_open()` helper if available.
- **JSON-to-clipboard export only** — opening as `file://` is acceptable.
- **Static read-only HTML** — open directly: `Start-Process "path/to/file.html"`.

## Authorship Marking

First line of every new version-controlled file:
- **Python:** `# Initially generated by Claude Code.`
- **Markdown/HTML:** `<!-- Initially generated by Claude Code. -->`

Does not apply to `.novc/` throwaway files.

## Minimum Font Size for Pointed Hebrew

Never use smaller than **20pt** for pointed Hebrew in generated HTML. All CSS rules for elements displaying pointed Hebrew must use `font-size: 20pt` or larger.

## Unicode Character Preservation

Never convert typographically correct Unicode to ASCII equivalents:
- Curly apostrophe `'` (U+2019), not straight `'` (U+0027)
- Curly quotes `"` (U+201C) and `"` (U+201D), not straight `"` (U+0022)
- Hebrew characters, vowel points, cantillation marks — preserved exactly

When editing, read the file first and copy exact characters from existing content rather than retyping.

## Markdown Formatting

Do not use bare tildes (`~`) as "approximately" — Markdown treats text between two `~` as strikethrough. Write "approx." or escape: `\~`.

## Screenshots

"Most recent screenshot" means the most recent file (by last-write time) in `C:\Users\BenDe\OneDrive\Pictures\Screenshots`.

## GitHub Repository Owner

The owner is **bdenckla**. Use this for GitHub MCP queries. Confirm via `git remote -v` if unsure.

## Local Sibling Repositories

Most repos are cloned as siblings at `../repo-name`. Use relative paths (e.g. `../MAM-simple/...`) — do not hard-code absolute paths.

## Terminology: "Varika"

**Varika** = **U+FB1E HEBREW POINT JUDEO-SPANISH VARIKA** (Alphabetic Presentation Forms block), not U+05BF HEBREW POINT RAFE (main Hebrew block).

## Hebrew Unicode Mark Order — No NFC Normalization

**Never apply Unicode normalization (NFC, NFD, etc.) to Hebrew text.** NFC reorders combining marks, destroying the project's intentional mark order. If strings that should be equal aren't matching, ensure both use the project's standard mark order — do not paper over with `unicodedata.normalize`. See `.github/copilot-instructions.md` for the mark order specification and implementation references.

## Do Not Mention Private Repos in Public Repos

Some sibling repos are private. Never reference a private repo by name in commits, code, docs, or issue/PR text destined for a public repo.

## Viewing a Word in Aleppo Codex Images

To show a zoomed-in Aleppo Codex image for a specific word, use `py/main_find_word_in_aleppo_images.py`:

```bash
.venv/Scripts/python.exe py/main_find_word_in_aleppo_images.py <book> <c:v> "<word>"
```

Example: `.venv/Scripts/python.exe py/main_find_word_in_aleppo_images.py Job 3:17 "יָ֝נ֗וּחוּ"`

The script looks up the word in line-break data, crops the page image around it with a fade overlay, generates an HTML preview in `.novc/`, and opens it in the browser. Use `--wide` for a wider crop. Book defaults to Job if omitted.

## Detailed Reference Files

- **`.github/copilot-instructions.md`** — project overview, pipeline stages, naming conventions, Hebrew mark order
- **`.github/copilot-instructions-mam-simple.md`** — MAM-simple XML format, verse extraction, versification traditions
- **`.github/copilot-instructions-mam-with-doc.md`** — MAM with Doc URLs and book codes
- **`.github/copilot-instructions-aleppo-line-breaks.md`** — line-break workflow, page image sources, Job leaf table
- **`.github/copilot-instructions-ocr.md`** — Kraken OCR setup and usage