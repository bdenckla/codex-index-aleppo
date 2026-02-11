"""
Spell check English text in HTML output files under docs/

Usage:
    python ./check_spelling_in_quirkrecs.py
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from spellchecker import SpellChecker


def load_custom_dictionary(dict_path: Path) -> tuple[set[str], list[str]]:
    """Load custom words and phrases from JSON dictionary file.

    Returns (words, phrases) where phrases are multi-word entries.
    """
    words = set()
    phrases = []
    if dict_path.exists():
        data = json.loads(dict_path.read_text(encoding="utf-8"))
        for word in data.get("words", []):
            # Normalize curly apostrophes to straight for lookup
            words.add(word.replace("\u2019", "'").lower())
        phrases = data.get("phrases", [])
    return words, phrases


def extract_english_words(text: str) -> list[str]:
    """Extract English words from text, ignoring Hebrew and sigla."""
    # Remove Hebrew characters (includes base letters, vowel points, accents, marks)
    text = re.sub(r"[\u0590-\u05FF]+", " ", text)
    # Remove $-prefixed sigla ($BHQ, $yod, $BHL_A, etc.)
    text = re.sub(r"\$[A-Za-z_]+", " ", text)
    # Extract words (letters including scholarly transliteration chars like š, ṣ, ḥ)
    # Include curly apostrophe (\u2019) as part of contractions (e.g. doesn\u2019t)
    # Include μ for sigla like μL, μA
    words = re.findall(r"[a-zA-ZšṣḥŠṢḤμ]+(?:\u2019[a-zA-Z]+)*", text)
    return words


class _TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping <style>, <script>, and Hebrew-only elements."""

    _SKIP_TAGS = {"style", "script"}

    def __init__(self):
        super().__init__()
        self._pieces: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            self._pieces.append(data)

    def get_text(self) -> str:
        return " ".join(self._pieces)


def _extract_text_from_html(html_path: Path) -> str:
    """Parse an HTML file and return its visible text content."""
    html = html_path.read_text(encoding="utf-8")
    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def _collect_html_files(docs_dir: Path) -> list[Path]:
    """Collect all .html files under docs/, recursively."""
    return sorted(docs_dir.rglob("*.html"))


def check_straight_apostrophes(html_files: list[Path]):
    """Check for straight apostrophes (U+0027) in HTML text; curly (\u2019) should be used."""
    issues = []
    for html_path in html_files:
        text = _extract_text_from_html(html_path)
        rel = html_path.as_posix()
        for match in re.finditer(r"'", text):
            context = text[max(0, match.start() - 10) : match.end() + 10]
            issues.append({"file": rel, "context": context})
    return issues


def check_period_uppercase(html_files: list[Path]):
    """Check for period immediately followed by an uppercase letter (missing space)."""
    issues = []
    for html_path in html_files:
        text = _extract_text_from_html(html_path)
        rel = html_path.as_posix()
        for match in re.finditer(r"\.[A-Z]", text):
            context = text[max(0, match.start() - 10) : match.end() + 10]
            issues.append({"file": rel, "context": context})
    return issues


def check_spelling(html_files: list[Path], custom_dict_path: Path):
    """Check spelling of English words in HTML files."""
    spell = SpellChecker()
    custom_words, custom_phrases = load_custom_dictionary(custom_dict_path)

    issues = []

    for html_path in html_files:
        text = _extract_text_from_html(html_path)
        rel = html_path.as_posix()

        # Normalize whitespace so phrase matching works
        # (the HTML text extractor can produce runs of whitespace)
        cleaned = re.sub(r"\s+", " ", text)

        # Remove accepted phrases before word extraction
        for phrase in custom_phrases:
            cleaned = re.sub(re.escape(phrase), " ", cleaned, flags=re.IGNORECASE)

        words = extract_english_words(cleaned)
        for word in words:
            word_lower = word.lower()
            # Normalize curly apostrophe to straight for pyspellchecker lookup
            lookup = word_lower.replace("\u2019", "'")
            if lookup not in custom_words and lookup not in spell:
                issues.append(
                    {
                        "file": rel,
                        "word": word,
                        "suggestions": list(spell.candidates(word_lower) or [])[:5],
                    }
                )

    return issues


def main():
    project_root = Path(__file__).parent
    docs_dir = project_root / "docs"
    custom_dict_path = (
        Path(__file__).parent / "check_spelling_in_html.custom-dict.json"
    )

    if not docs_dir.exists():
        print(f"Error: {docs_dir} not found")
        print("Run: python main_gen_misc_authored_english_documents.py")
        return

    html_files = _collect_html_files(docs_dir)
    if not html_files:
        print(f"Error: no HTML files found under {docs_dir}")
        return

    print(f"Checking spelling in {len(html_files)} HTML file(s) under {docs_dir}...")
    print(f"Using custom dictionary: {custom_dict_path}")

    apos_issues = check_straight_apostrophes(html_files)
    if apos_issues:
        print(
            f"\nFound {len(apos_issues)} straight-apostrophe issues (use \u2019 not '):\n"
        )
        for issue in apos_issues:
            print(f"  [{issue['file']}]: ...{issue['context']}...")

    period_issues = check_period_uppercase(html_files)
    if period_issues:
        print(
            f"\nFound {len(period_issues)} period-uppercase issues (missing space?):\n"
        )
        for issue in period_issues:
            print(f"  [{issue['file']}]: ...{issue['context']}...")

    issues = check_spelling(html_files, custom_dict_path)

    if issues:
        print(f"\nFound {len(issues)} potential spelling issues:\n")
        for issue in issues:
            print(f"  [{issue['file']}]: '{issue['word']}'")
            if issue["suggestions"]:
                print(f"    Suggestions: {', '.join(issue['suggestions'])}")

        # Group by word
        word_counts = {}
        for issue in issues:
            word = issue["word"].lower()
            word_counts[word] = word_counts.get(word, 0) + 1

        print("\n--- Summary by word ---")
        for word, count in sorted(word_counts.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count} occurrence(s)")
    else:
        print("\nNo spelling issues found!")

    if apos_issues or period_issues or issues:
        exit(1)


if __name__ == "__main__":
    main()
