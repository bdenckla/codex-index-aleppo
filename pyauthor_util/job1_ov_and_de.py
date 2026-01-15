""" Exports make_ov_and_de_for_all_records, make_example_row """

from py import my_html
from pyauthor.common import D1D_FNAME
from pyauthor_util import author
from pyauthor_util.job1_highlight import highlight, color
from pyauthor_util.job1_lcloc import lcloc
from pyauthor_util.job1_records import RECORDS
from pycmn.my_utils import sl_map


def make_ov_and_de_for_all_records():
    ids = sl_map(_row_id, RECORDS)
    assert _unique(ids)
    return sl_map(_make_ov_and_de_for_one_record, RECORDS)


def _unique(seq):
    return len(set(seq)) == len(seq)


def _make_ov_and_de_for_one_record(record):
    return {
        "od-overview": make_overview_row(record),
        "od-details": _make_details_row(record),
    }


def make_example_row():
    hlc = color("μL", "lc")
    hmam = color("consensus", "mam")
    lc_and_mam = [hlc, my_html.line_break(), hmam]
    return my_html.table_row(
        [
            my_html.table_datum(lc_and_mam),
            my_html.table_datum("c:v"),
            my_html.table_datum("how μL differs from consensus"),
        ]
    )


def _lc_and_mam(record):
    hlc = highlight(record, "lc")
    hmam = highlight(record, "mam")
    if lc_q := record.get("lc-q"):
        assert lc_q == "(?)"
        lc_and_q = [hlc, " (?)"]
    else:
        lc_and_q = [hlc]
    lc_and_mam = [*lc_and_q, my_html.line_break(), hmam]
    return lc_and_mam


def make_overview_row(record):
    hbo_attrs = {"lang": "hbo", "dir": "rtl"}
    row_id = _row_id(record)
    anc = my_html.anchor_h("#", f"{D1D_FNAME}#{row_id}")  # self-anchor
    tr_contents = [
        my_html.table_datum(anc),
        my_html.table_datum(_lc_and_mam(record), hbo_attrs),
        my_html.table_datum(record["cv"]),
        my_html.table_datum(record["what-is-weird"]),
    ]
    tr_attrs = {"id": row_id}
    return my_html.table_row(tr_contents, tr_attrs)


def _row_id(record):
    nn_v_mm = record["cv"].replace(":", "v")
    return f"row-{nn_v_mm}"


def _img(img):
    return my_html.img({"src": f"img/{img}"})


_MI_ARGS = {
    "mi-args-aleppo": [
        "μA (Aleppo)",
        "aleppo-img-intro",
        "aleppo-img",
    ],
    "mi-args-cam1753": [
        "μY (Cambridge 1753)",
        "cam1753-img-intro",
        "cam1753-img",
    ],
}


def _maybe_img(record, mi_args):
    ms_name, iikey, ipkey = _MI_ARGS[mi_args]
    maybe_img_path = record.get(ipkey)
    if maybe_img_path is None:
        return []
    if maybe_img_intro := record.get(iikey):
        intro = f" ({maybe_img_intro})"
    else:
        intro = ""
    cpara = f"{ms_name}{intro}:"
    return [my_html.para(cpara), _img(maybe_img_path)]


def _maybe_bhq(bhq):
    if bhq is None:
        return []
    cont_p = ["BHQ: ", author.hbo(bhq)]
    return [my_html.para(cont_p)]


_DEFAULT_BHQ_COMMENT = (
    "BHQ agrees with μL here, but BHQ makes no note of μL’s divergence from consensus."
)
_SEP = " \N{EM DASH} "


def _maybe_sep_lc_is_from_bhla(record):
    if record.get("bhla-i"):
        return [_SEP, "μL is from BHL-A"]
    return []


def _maybe_sep_comment(record):
    if comment := record.get("comment"):
        return [_SEP, comment]
    return []


def _sep_bhq_comment(record):
    bhq_comment = record.get("bhq-comment") or _DEFAULT_BHQ_COMMENT
    return [_SEP, bhq_comment]


def _make_details_row(record):
    cv = record["cv"]
    uxlc_href = f"https://tanach.us/Tanach.xml?Job{cv}"
    uxlc_anc = my_html.anchor_h("UXLC", uxlc_href)
    cnvm = "c" + cv.replace(":", "v")
    mwd_href = f"https://bdenckla.github.io/MAM-with-doc/D3-Job.html#{cnvm}"
    mwd_anc = my_html.anchor_h("MwD", mwd_href)
    dpe = [
        uxlc_anc,
        _SEP,
        mwd_anc,
        _SEP,
        *lcloc(record.get("lc-loc")),
        *_maybe_sep_comment(record),
        *_sep_bhq_comment(record),
        *_maybe_sep_lc_is_from_bhla(record),
    ]
    return [
        author.table_c(make_overview_row(record)),
        *_maybe_bhq(record.get("bhq")),
        author.para(dpe),
        _img(record["lc-img"]),
        *_maybe_img(record, "mi-args-aleppo"),
        *_maybe_img(record, "mi-args-cam1753"),
        my_html.horizontal_rule(),
    ]
