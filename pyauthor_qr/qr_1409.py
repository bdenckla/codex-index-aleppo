from pyauthor_util.job_common import core_ignores


RECORD_1409 = {
    "qr-bhla-i": 18,
    "qr-cv": "14:9",
    "qr-lc-proposed": "מֵרֵ֣יַּח",
    "qr-what-is-weird": "$yod has דגש",
    "qr-consensus": "מֵרֵ֣יחַ",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "401A", "column": 1, "line": -9},
    "qr-generic-comment": [
        "The possible דגש looks slightly different than nearby dots in the two ציריה vowels."
        " This raises the possibility that it is not ink, e.g. a speck on the vellum.",
    ],
    "qr-bhq-comment": [
        "$BHQ silently ignores the possible דגש.",
        [" ", *core_ignores()],
    ],
    "qr-noted-by": "nBHL",
}
