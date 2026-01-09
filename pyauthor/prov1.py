""" Exports main """

from pycmn.my_utils import sl_map
from py import my_html
from pyauthor.util import author
from pyauthor.prov1_table import TABLE


def anchor(provn_dir="."):
    anc = my_html.anchor_h("document", f"{provn_dir}/{_FNAME}")
    return author.std_anchor(anc, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, _CBODY)


def _make_row(record):
    if blha_q := record["bhla-q"]:
        assert blha_q == "(?)"
        bhla_and_q = [record["bhla"], " (?)"]
    else:
        bhla_and_q = [record["bhla"]]
    bhla_and_mam = [*bhla_and_q, my_html.line_break(), record["mam"]]
    hbo_attrs = {"lang": "hbo", "dir": "rtl"}
    return my_html.table_row(
        [
            # str(record["bhla-i"]),
            my_html.table_datum(record["cv"]),
            my_html.table_datum(bhla_and_mam, hbo_attrs),
            my_html.table_datum(record["what-is-weird"]),
            # record["comment"],
        ]
    )


_TITLE = "Proverbs Document 1"
_H1_CONTENTS = "Proverbs (משלי) Document 1"
_FNAME = "prov1.html"
_CONT_PARA_01 = [
    "Here is a table expanding upon the entries for Proverbs",
    " in BHL Appendix A.",
]
_CONT_TABLE_1A_ROWS = sl_map(_make_row, TABLE)
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para(_CONT_PARA_01),
    author.table_c(_CONT_TABLE_1A_ROWS),
]
