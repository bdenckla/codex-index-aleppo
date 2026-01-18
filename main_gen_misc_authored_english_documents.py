""" Exports main """

from py import two_col_css_styles as tcstyles
from py import my_html
from pyauthor import job1_overview
from pyauthor import job1_details
from pyauthor import job2
from pyauthor.common import d2_anchor
from pyauthor_util.job1_quirkrecs import QUIRKRECS
from pyauthor_util.job1_ov_and_de import make_ov_and_de_for_all_quirkrecs, sort_key


def write_index_dot_html(css_hrefs, out_path):
    write_ctx = my_html.WriteCtx("Job Documents", out_path, css_hrefs=css_hrefs)
    my_html.write_html_to_file(_CBODY, write_ctx)


def main():
    # XXX TODO: rm *.html (to avoid stale files when output names change)
    #
    jobn_rel_top = "docs/jobn"
    css_href = "style.css"
    tcstyles.make_css_file_for_authored(f"docs/{css_href}")
    tcstyles.make_css_file_for_authored(f"{jobn_rel_top}/{css_href}")
    #
    tdm_ch = jobn_rel_top, css_href
    #
    qrs = sorted(QUIRKRECS, key=sort_key)
    ov_and_de = make_ov_and_de_for_all_quirkrecs(qrs)
    job1_overview.gen_html_file(tdm_ch, ov_and_de)
    job1_details.gen_html_file(tdm_ch, ov_and_de)
    job2.gen_html_file(tdm_ch, ov_and_de, qrs)
    #
    write_index_dot_html((css_href,), "docs/index.html")


_CBODY = [
    "Currently this repository hosts only one",
    " ",
    d2_anchor("./jobn"),
]


if __name__ == "__main__":
    main()
