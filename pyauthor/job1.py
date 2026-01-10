""" Exports gen_html_file and anchor """

from pycmn.my_utils import sl_map
from py import my_html
from pyauthor.util import author
from pyauthor.job1_records import RECORDS
from pyauthor.job1_make_per_case_data import make_per_case_data


def anchor(jobn_dir="."):
    anc = my_html.anchor_h("document", f"{jobn_dir}/{_FNAME}")
    return author.std_anchor(anc, _H1_CONTENTS)


def gen_html_file(tdm_ch, jda):
    author.assert_stem_eq(__file__, _FNAME)
    jdae = [" ", jda, "."]
    _CONT_PARA_01 = [
        "Here is a table expanding upon the entries for the book of Job",
        " in BHL Appendix A.",
        " For more details, see the",
        jdae,
    ]
    _CBODY = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_CONT_PARA_01),
        author.table_c(_CONT_TABLE_1A_ROWS),
    ]
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, _CBODY)


_TITLE = "Book of Job Document 1"
_H1_CONTENTS = "Book of Job (ספר איוב) Document 1"
_FNAME = "job1.html"
_PER_CASE_DATA = sl_map(make_per_case_data, RECORDS)
_CONT_TABLE_1A_ROWS = [pcd["row"] for pcd in _PER_CASE_DATA]
