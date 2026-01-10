""" Exports main """

import re
from pycmn.my_utils import sl_map
from py import my_html
from pyauthor.util import author
from pyauthor.job1_records import RECORDS


def anchor(jobn_dir="."):
    anc = my_html.anchor_h("document", f"{jobn_dir}/{_FNAME}")
    return author.std_anchor(anc, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, _CBODY)


def _highlight(record, key):
    zbhls = _zb_highlights(record, key)  # zero-based highlights
    rk = record[key]
    clusters = re.findall(r"[א-ת][^א-ת]*", rk)
    jc = "".join(clusters)
    assert jc == rk
    color = _RK_COLOR[key]
    out = [cl if i not in zbhls else _color(cl, color) for i, cl in enumerate(clusters)]
    return out


def _zb_highlights(record, key):
    hl_both = record.get("highlight")
    hl_spec = record.get(_RK_HL_SPECIFIC[key])
    assert (hl_both is None) or (hl_spec is None)
    hl = hl_both or hl_spec
    if isinstance(hl, int):
        return [hl - 1]
    assert isinstance(hl, list)
    return [obi - 1 for obi in hl]


def _color(text, color):
    return my_html.span(text, {"style": f"color: {color}"})


_RK_COLOR = {
    "bhla": "red",
    "mam": "green",
}
_RK_HL_SPECIFIC = {
    "bhla": "highlight-bhla",
    "mam": "highlight-mam",
}


def _make_row(record):
    hbhla = _highlight(record, "bhla")
    hmam = _highlight(record, "mam")
    if blha_q := record["bhla-q"]:
        assert blha_q == "(?)"
        bhla_and_q = [hbhla, " (?)"]
    else:
        bhla_and_q = [hbhla]
    bhla_and_mam = [*bhla_and_q, my_html.line_break(), hmam]
    hbo_attrs = {"lang": "hbo", "dir": "rtl"}
    return my_html.table_row(
        [
            # str(record["bhla-i"]),
            my_html.table_datum(bhla_and_mam, hbo_attrs),
            my_html.table_datum(record["cv"]),
            my_html.table_datum(record["what-is-weird"]),
        ]
    )


def _make_details(record):
    cv = record["cv"]
    uxlc_href = f"https://tanach.us/Tanach.xml?Job{cv}"
    uxlc_anc = my_html.anchor_h("UXLC", uxlc_href)
    cnvm = "c" + cv.replace(":", "v")
    mwd_href = f"https://bdenckla.github.io/MAM-with-doc/D3-Job.html#{cnvm}"
    mwd_anc = my_html.anchor_h("MwD", mwd_href)
    comment = record["comment"]
    details_proper = my_html.para([uxlc_anc, " ", mwd_anc, " ", comment])
    return [author.table_c(_make_row(record)), details_proper]


def _make_per_case_data(record):
    return {
        "row": _make_row(record),
        "details": _make_details(record),
    }


_TITLE = "Book of Job Document 1"
_H1_CONTENTS = "Book of Job (ספר איוב) Document 1"
_FNAME = "job1.html"
_CONT_PARA_01 = [
    "Here is a table expanding upon the entries for the book of Job",
    " in BHL Appendix A.",
]
_PER_CASE_DATA = sl_map(_make_per_case_data, RECORDS)
_CONT_TABLE_1A_ROWS = [pcd["row"] for pcd in _PER_CASE_DATA]
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para(_CONT_PARA_01),
    author.table_c(_CONT_TABLE_1A_ROWS),
]
