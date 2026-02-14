# Aleppo Codex Alignment JSON Format

## Overview

Each `py_ac_loc/aleppo_col_lines_{leaf}.json` file records the line-by-line
alignment of one Aleppo Codex page image to the corresponding MAM-XML text.

## Consistency Checker

After editing any alignment JSON file, run:

```
python py_ac_loc/check_aleppo_col_lines.py
```

This validates that all redundant/friendly fields are consistent with their
machine-readable counterparts.

## Top-Level Keys

| Key | Type | Description |
|-----|------|-------------|
| `leaf` | string | Leaf identifier, e.g. `"281v"` |
| `description` | list of strings | Generic description (same in every file) |
| `ranges-covered-by-this-page` | list of range objects | Overall text extent of the page in machine-readable form, split per book (see [Range Object](#range-object)) |
| `ranges-covered-by-this-page-friendly` | list of ranges-friendly objects | Human-readable version of `ranges-covered-by-this-page` (see [Ranges-Friendly](#ranges-friendly-format)). **Redundant** — must match `ranges-covered-by-this-page`. |
| `MAM-XML source file(s)` | list of strings | Repo-relative paths to source XML files, e.g. `"MAM-XML/out/xml-vtrad-mam/Job.xml"` |
| `page_image` | string | URL to the page image on archive.org |
| `column_1` | object | Metadata for the right column (see [Column Object](#column-object)) |
| `column_2` | object | Metadata for the left column (see [Column Object](#column-object)) |
| `column_1_lines` | list of line objects | Line data for column 1 (see [Line Data](#line-data)) |
| `column_2_lines` | list of line objects | Line data for column 2 (see [Line Data](#line-data)) |

## Column Object

Each column object (`column_1`, `column_2`) contains:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `side` | string | yes | `"right"` for column 1, `"left"` for column 2 |
| `ranges-covered-by-this-column` | list of range objects | yes | Machine-readable text ranges (see [Range Object](#range-object)) |
| `ranges-covered-by-this-column-friendly` | list of ranges-friendly objects | yes | Human-readable version of `ranges-covered-by-this-column` (see [Ranges-Friendly](#ranges-friendly-format)). **Redundant** — must match `ranges-covered-by-this-column`. |
| `line_count` | integer | yes | Number of lines in the column (typically 28) |
| `blank_lines` | list of integers | if any | Line numbers that are blank (empty string). Used at book boundaries. |
| `pe_lines` | list of integers | if any | Line numbers containing only `{פ}` (parashah pe break). |
| `ketivs` | list of ketiv objects | if any | Ketiv readings in this column (see [Ketiv Object](#ketiv-object)) |
| `notes` | list of strings | if any | Free-form English notes for anything not captured by the structured fields above |

Keys are omitted when the list would be empty (`blank_lines`, `pe_lines`,
`ketivs`, `notes`).

## Range Object

Each range object represents a contiguous text span within one book:

```json
{
  "start": ["Job", 41, 23, "first-word"],
  "end": ["Job", 42, 10, "first-word"]
}
```

Each endpoint is a 4-element array: `[book, chapter, verse, fml]`

The `fml` (first/middle/last) value indicates where the column boundary falls
within the verse:

| Value | Meaning |
|-------|---------|
| `"first-word"` | The column starts/ends at the first word of this verse |
| `"a-middle-word"` | The column starts/ends at a middle word (verse is split across columns) |
| `"last-word"` | The column starts/ends at the last word of this verse |

**Cross-book ranges** are split into separate within-book range objects.
For example, a column spanning Job 42:11–Prov 1:8 has two range objects:
one for `Job 42:11–42:17` and one for `Prov 1:1–1:8`.

## Ranges-Friendly Format

A human-readable mirror of the machine-readable range. Each endpoint becomes
a single string:

```json
{
  "start": "Job 41:23-first",
  "end": "Job 42:10-first"
}
```

The suffix mapping is:

| Machine-readable | Friendly suffix |
|-----------------|----------------|
| `"first-word"` | `-first` |
| `"a-middle-word"` | `-mid` |
| `"last-word"` | `-last` |

The top-level `"ranges-covered-by-this-page"` uses the machine-readable
range-object format, and `"ranges-covered-by-this-page-friendly"` uses the
ranges-friendly format. Both are lists of range objects (one per book),
derived by merging all column ranges across both columns and grouping by book.

## Ketiv Object

Records a ketiv (written) reading that differs from the qere (read) form:

```json
{
  "bcv-fml": ["Job", 42, 2, "first-word"],
  "bcv-fml-friendly": "Job 42:2-first",
  "word": "ידעת"
}
```

| Key | Type | Description |
|-----|------|-------------|
| `bcv-fml` | 4-element array | `[book, chapter, verse, fml]` — locates the ketiv word |
| `bcv-fml-friendly` | string | Human-readable version. **Redundant** — must match `bcv-fml`. |
| `word` | string | The ketiv word as it appears in the manuscript (unpointed or partially pointed) |

The `fml` value here indicates where the ketiv word falls within its verse
(first word, a middle word, or last word).

## Line Data

Each `column_N_lines` array contains objects with the following fields:

| Key | Type | Description |
|-----|------|-------------|
| `line-num` | integer | 1-based line number, sequential |
| `range` | `[string, string]` or `null` | Verse range on this line (see below), or `null` for blank/{פ} lines |
| `MAM-XML-fragment` | string | The text content of the line |

```json
[
  {"line-num": 1, "range": ["Job 41:23-first", "Job 41:23-last"], "MAM-XML-fragment": "יַרְתִּ֙יחַ כַּסִּ֙יר מְצוּלָ֑ה יָם׀ח יָשִׂ֥ים כַּמֶּרְקָחָֽה׃"},
  {"line-num": 2, "range": ["Job 41:24-first", "Job 41:24-last"], "MAM-XML-fragment": "אַ֭חֲרָיו יָאִ֙יר נָתִ֑יב יַחְשֹׁ֖ב תְּה֙וֹם לְשֵׂיבָֽה׃"},
  {"line-num": 3, "range": ["Job 41:25-mid", "Job 41:26-mid"], "MAM-XML-fragment": "אֵֽין־עַל־עָפָ֥ר ..."},
  ...
]
```

The **range** field is either `null` or a 2-element `[start, end]`
array indicating the verse range that appears on that line.

Each endpoint is a string in the format `"Book ch:vs-qualifier"` where the
qualifier indicates the word position within the verse:

| Qualifier | Meaning |
|-----------|---------|
| `-first` | The line includes the first word of this verse |
| `-mid` | The line starts/ends at a middle word (neither first nor last) |
| `-last` | The line includes the last word of this verse |

Examples:

| Range | Meaning |
|-------|---------|
| `["Job 41:23-first", "Job 41:23-last"]` | Full verse on one line |
| `["Job 1:1-first", "Job 1:1-mid"]` | First part of a verse |
| `["Job 1:1-mid", "Job 1:1-last"]` | Last part of a verse |
| `["Job 1:7-mid", "Job 1:8-mid"]` | End of one verse + start of the next |
| `null` | Blank line or {פ}-only line |

Special line types:
- **Blank line:** `{"line-num": 17, "range": null, "MAM-XML-fragment": ""}` — used at book boundaries
- **Pe-only line:** `{"line-num": 5, "range": null, "MAM-XML-fragment": "{פ}"}` — parashah pe break occupying an entire line
- **Pe within text:** `{"line-num": 6, "range": ["Job 1:5-mid", "Job 1:5-last"], "MAM-XML-fragment": "כָּכָה יַעֲשֶׂ֥ה אִיֹּ֖ב כָּל־הַיָּמִֽים׃ {פ}"}` — pe marker at end of a text line

Line numbers are 1-based and sequential.
## Redundancy

Several fields are intentionally redundant to aid human readability:

| Friendly field | Must match |
|----------------|-----------|
| `ranges-covered-by-this-column-friendly` | `ranges-covered-by-this-column` |
| `ranges-covered-by-this-page` | `ranges-covered-by-this-page-friendly` (machine ↔ friendly) |
| `ranges-covered-by-this-page-friendly` | Merge of all column `ranges-covered-by-this-column-friendly` entries, grouped by book |
| `bcv-fml-friendly` (in ketivs) | `bcv-fml` |
| `blank_lines` | Lines in `column_N_lines` with empty text |
| `pe_lines` | Lines in `column_N_lines` with text `"{פ}"` |
| ketiv `word` | Must appear in some line in `column_N_lines` |
| line range | `null` for blank/{פ} lines; non-null `[start, end]` range pair for text lines |

Run `python py_ac_loc/check_aleppo_col_lines.py` to verify all of these.

## Example (Minimal Column)

```json
{
  "side": "right",
  "ranges-covered-by-this-column": [
    {
      "start": ["Job", 32, 8, "first-word"],
      "end": ["Job", 33, 11, "first-word"]
    }
  ],
  "ranges-covered-by-this-column-friendly": [
    {
      "start": "Job 32:8-first",
      "end": "Job 33:11-first"
    }
  ],
  "line_count": 28
}
```

## Example (Column with All Optional Fields)

```json
{
  "side": "right",
  "ranges-covered-by-this-column": [
    {
      "start": ["Job", 41, 23, "first-word"],
      "end": ["Job", 42, 10, "first-word"]
    }
  ],
  "ranges-covered-by-this-column-friendly": [
    {
      "start": "Job 41:23-first",
      "end": "Job 42:10-first"
    }
  ],
  "line_count": 28,
  "pe_lines": [5, 14],
  "ketivs": [
    {
      "bcv-fml": ["Job", 42, 2, "first-word"],
      "bcv-fml-friendly": "Job 42:2-first",
      "word": "ידעת"
    },
    {
      "bcv-fml": ["Job", 42, 10, "a-middle-word"],
      "bcv-fml-friendly": "Job 42:10-mid",
      "word": "אֶת־שבית"
    }
  ]
}
```
