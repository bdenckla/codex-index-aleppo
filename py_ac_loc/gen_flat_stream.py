"""
Generate flat-stream JSON files for Aleppo Codex pages.

Each page gets a JSON file containing a flat array of:
  - structural markers: {"page-start": "280v"}, {"page-end": "280v"}
  - verse markers: {"verse-start": "Job 38:31"}, {"verse-end": "Job 38:31"}
  - parashah markers: {"parashah": "spi-pe2"}, {"parashah": "spi-samekh2"}
  - words: plain Hebrew strings

Column and line markers are NOT pre-populated — the user adds them
interactively via the HTML editor.

Verse ranges come from codex-index/index-flat.json (full verses).

Usage:
    python .novc/gen_flat_stream.py              # all pages
    python .novc/gen_flat_stream.py 280v         # one page
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from py_ac_loc.mam_xml_verses import get_verses_in_range
from pycmn.uni_denorm import has_std_mark_order

BASE = Path(__file__).resolve().parent.parent
AC_DIR = BASE / "py_ac_loc"
MAM_XML_DIR = BASE / "MAM-XML"
INDEX_PATH = AC_DIR / "codex-index" / "index-flat.json"
OUT_DIR = BASE / "ds-flat-stream"

BOOK_XML = {
    "Job": "Job.xml",
    "Ps": "Ps.xml",
    "Prov": "Prov.xml",
}

# Pages we care about
OUR_PAGES = [
    "270r",
    "278v",
    "279r",
    "279v",
    "280r",
    "280v",
    "281r",
    "281v",
]

# For cross-book pages we need to know where each book ends
# (last chapter, last verse). We'll use large sentinels and
# let the XML parser handle it.
BOOK_END_SENTINEL = (999, 999)
BOOK_START = (1, 1)


def load_index():
    """Load the codex-index and return a dict: leaf -> de_text_range."""
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    result = {}
    for row in data["body"]:
        result[row["de_leaf"]] = row["de_text_range"]
    return result


def get_page_verses(text_range):
    """Fetch all verses for a page from MAM-XML, handling cross-book pages.

    Args:
        text_range: [[book, ch, vs], [book, ch, vs]] pair from
            index-flat.json, giving the start and end of the page’s
            text coverage.

    Returns:
        List of verse dicts, each with keys: book, cv, words,
        ketiv_indices, parashah_after.
    """
    start_book, start_ch, start_vs = text_range[0]
    end_book, end_ch, end_vs = text_range[1]

    if start_book == end_book:
        # Same book — simple case
        xml_path = str(MAM_XML_DIR / BOOK_XML[start_book])
        verses = get_verses_in_range(
            xml_path,
            start_book,
            (start_ch, start_vs),
            (end_ch, end_vs),
        )
        for v in verses:
            v["book"] = start_book
        return verses
    else:
        # Cross-book page (e.g., Ps→Job or Job→Prov)
        all_verses = []

        # First book: from start_cv to end of book
        xml_path = str(MAM_XML_DIR / BOOK_XML[start_book])
        verses1 = get_verses_in_range(
            xml_path,
            start_book,
            (start_ch, start_vs),
            BOOK_END_SENTINEL,
        )
        for v in verses1:
            v["book"] = start_book
        all_verses.extend(verses1)

        # Second book: from start of book to end_cv
        xml_path = str(MAM_XML_DIR / BOOK_XML[end_book])
        verses2 = get_verses_in_range(
            xml_path,
            end_book,
            BOOK_START,
            (end_ch, end_vs),
        )
        for v in verses2:
            v["book"] = end_book
        all_verses.extend(verses2)

        return all_verses


MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"


def _assert_standard_order(word, verse_label):
    """Assert combining marks on each base letter follow standard order.

    Uses pycmn.uni_denorm.has_std_mark_order (SBL2 mark order) to check
    that the word already has the project’s standard mark ordering.

    Args:
        word: a single Hebrew word string (base letters + combining marks).
        verse_label: human-readable verse label (e.g. "Job 38:1") for
            error messages.
    """
    if not has_std_mark_order(word):
        marks_str = " ".join(
            f"U+{ord(c):04X}" for c in word if ord(c) > 0x0590 and ord(c) < 0x05F5
        )
        raise AssertionError(
            f"Non-standard combining mark order in {verse_label}, "
            f"word ‘{word}’. Marks: [{marks_str}]"
        )


def build_flat_stream(page_id, verses):
    """Build the flat stream array for a page.

    Args:
        page_id: leaf identifier, e.g. "270r".
        verses: list of verse dicts as returned by get_page_verses.

    Returns:
        The flat stream list (strings and marker dicts).
    """
    stream = []
    stream.append({"page-start": page_id})

    for v in verses:
        book = v["book"]
        cv = v["cv"]
        label = f"{book} {cv}"

        if v.get("parashah_before"):
            stream.append(v["parashah_before"])

        stream.append({"verse-start": label})
        for word in v["words"]:
            _assert_standard_order(word, label)
            # Split at maqaf keeping the maqaf attached
            # to the preceding fragment: "אֽוֹ־מֹשְׁכִּזוֹת" → ["אֽוֹ־", "מֹשְׁכִּזוֹת"]
            parts = word.split(MAQAF)
            for k, part in enumerate(parts):
                if k < len(parts) - 1:
                    stream.append(part + MAQAF)
                else:
                    stream.append(part)
        stream.append({"verse-end": label})

    stream.append({"page-end": page_id})
    return stream


def write_stream(page_id, stream):
    """Write the flat stream JSON file.

    Args:
        page_id: leaf identifier, e.g. "270r".
        stream: flat stream list to serialize.
    """
    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{page_id}.json"
    out_path.write_text(
        json.dumps(stream, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out_path


def main():
    index = load_index()

    if len(sys.argv) > 1:
        pages_set = set(sys.argv[1:])
    else:
        pages_set = set(OUR_PAGES)

    for page_id in OUR_PAGES:
        if page_id not in index:
            print(f"WARNING: {page_id} not found in index-flat.json")
            continue
        text_range = index[page_id]
        print(f"{page_id}: {text_range[0]} .. {text_range[1]}")
        verses = get_page_verses(text_range)
        stream = build_flat_stream(page_id, verses)

        if page_id in pages_set:
            word_count = sum(1 for x in stream if isinstance(x, str))
            verse_count = sum(
                1 for x in stream if isinstance(x, dict) and "verse-start" in x
            )
            out_path = write_stream(page_id, stream)
            print(f"  -> {out_path.name}: {verse_count} verses, {word_count} words")
        else:
            print(f"  (skipped, not in requested pages)")


if __name__ == "__main__":
    main()
