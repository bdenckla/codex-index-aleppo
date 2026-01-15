from pyauthor_util import author
from pyauthor_util.job1_make_per_case_data import make_example_row


def intro(ov_or_de, jda=None):
    start, each = _VARIANTS[ov_or_de]
    return [
        author.para(_here_is(start, jda)),
        author.para(_each(each)),
        author.table_c(make_example_row()),
        author.para(_where()),
    ]


_VARIANTS = {
    "overview": ("Below is a table summarizing", "Each"),
    "details": ("This document presents", "The header of each"),
}


def _here_is(start, jda=None):
    out = [
        f"{start} some quirks in μL in the book of Job.",
    ]
    if jda is not None:
        jdae = [" For more details, see the ", jda]
        return out + jdae
    return out


def _each(each):
    return [f"{each} entry below takes the following form:"]


def _where():
    return [
        "Where c:v is the chapter and verse of the book of Job and μL is the contents of the Leningrad Codex (or the best guess of it)."
    ]
