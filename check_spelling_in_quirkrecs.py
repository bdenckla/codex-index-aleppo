"""
Spell check English strings in quirkrecs.json

Usage:
    python ./spellcheck_quirkrecs.py
"""

import json
import re
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


# Fields that contain English prose to spell-check
PROSE_FIELDS = {
    "qr-bhq-comment",
    "qr-generic-comment",
    "qr-what-is-weird",
}


def _collect_strings(value):
    """Yield all plain strings from a nested structure (str, list, or dict with contents)."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _collect_strings(item)
    elif isinstance(value, dict) and "contents" in value:
        yield from _collect_strings(value["contents"])


def check_straight_apostrophes(quirkrecs_path: Path):
    """Check for straight apostrophes (U+0027) in prose fields; curly (\u2019) should be used."""
    with open(quirkrecs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = []
    for rec in data:
        rec_id = rec.get("qr-id", "unknown")
        for key, value in rec.items():
            if key not in PROSE_FIELDS:
                continue
            for text in _collect_strings(value):
                for match in re.finditer(r"'", text):
                    context = text[max(0, match.start() - 10) : match.end() + 10]
                    issues.append(
                        {
                            "record": rec_id,
                            "field": key,
                            "context": context,
                        }
                    )
    return issues


def check_period_uppercase(quirkrecs_path: Path):
    """Check for period immediately followed by an uppercase letter (missing space)."""
    with open(quirkrecs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = []
    for rec in data:
        rec_id = rec.get("qr-id", "unknown")
        for key, value in rec.items():
            if key not in PROSE_FIELDS:
                continue
            for text in _collect_strings(value):
                for match in re.finditer(r"\.[A-Z]", text):
                    context = text[max(0, match.start() - 10) : match.end() + 10]
                    issues.append(
                        {
                            "record": rec_id,
                            "field": key,
                            "context": context,
                        }
                    )
    return issues


def check_spelling(quirkrecs_path: Path, custom_dict_path: Path):
    """Check spelling of English words in quirkrecs.json."""
    spell = SpellChecker()
    custom_words, custom_phrases = load_custom_dictionary(custom_dict_path)

    with open(quirkrecs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = []

    for rec in data:
        rec_id = rec.get("qr-id", "unknown")

        # Check prose fields only
        for key, value in rec.items():
            if key not in PROSE_FIELDS:
                continue
            for text in _collect_strings(value):
                # Remove accepted phrases before word extraction
                cleaned = text
                for phrase in custom_phrases:
                    cleaned = re.sub(
                        re.escape(phrase), " ", cleaned, flags=re.IGNORECASE
                    )
                words = extract_english_words(cleaned)
                for word in words:
                    word_lower = word.lower()
                    # Normalize curly apostrophe to straight for pyspellchecker lookup
                    lookup = word_lower.replace("\u2019", "'")
                    if lookup not in custom_words and lookup not in spell:
                        issues.append(
                            {
                                "record": rec_id,
                                "field": key,
                                "word": word,
                                "suggestions": list(spell.candidates(word_lower) or [])[
                                    :5
                                ],
                            }
                        )

    return issues


def main():
    project_root = Path(__file__).parent
    quirkrecs_path = project_root / "out" / "quirkrecs.json"
    custom_dict_path = (
        Path(__file__).parent / "check_spelling_in_quirkrecs.custom-dict.json"
    )

    if not quirkrecs_path.exists():
        print(f"Error: {quirkrecs_path} not found")
        print("Run: python main_gen_misc_authored_english_documents.py")
        return

    print(f"Checking spelling in {quirkrecs_path}...")
    print(f"Using custom dictionary: {custom_dict_path}")

    apos_issues = check_straight_apostrophes(quirkrecs_path)
    if apos_issues:
        print(
            f"\nFound {len(apos_issues)} straight-apostrophe issues (use \u2019 not '):\n"
        )
        for issue in apos_issues:
            print(f"  [{issue['record']}] {issue['field']}: ...{issue['context']}...")

    period_issues = check_period_uppercase(quirkrecs_path)
    if period_issues:
        print(
            f"\nFound {len(period_issues)} period-uppercase issues (missing space?):\n"
        )
        for issue in period_issues:
            print(f"  [{issue['record']}] {issue['field']}: ...{issue['context']}...")

    issues = check_spelling(quirkrecs_path, custom_dict_path)

    if issues:
        print(f"\nFound {len(issues)} potential spelling issues:\n")
        for issue in issues:
            print(f"  [{issue['record']}] {issue['field']}: '{issue['word']}'")
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
