from pyauthor_util.job_common import correctly_ignores


_COMMENT_3629 = [
    "The color image strongly suggests that the mark in question is not ink.",
    " A געיה right next to סילוק like that would be extraordinary, by the way,",
    " though no appeal to expectations is needed to dismiss this possible געיה.",
]
RECORD_3629 = {
    "bhla-i": 43,
    "cv": "36:29",
    "qr-lc-proposed": "סֻכָּֽתֽוֹ׃",
    "what-is-weird": "כ has געיה",
    "qr-consensus": "סֻכָּתֽוֹ׃",
    "comment": _COMMENT_3629,
    "highlight": 2,
    "lc-loc": {"page": "407B", "column": 1, "line": -5},
    "bhq-comment": correctly_ignores("געיה", "36:29", "large"),
    "noted-by": "tBHQ-nBHL-xDM",
}
