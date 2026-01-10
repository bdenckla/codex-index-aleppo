""" Exports highlight """

import re
from py import my_html


def highlight(record, key):
    zbhls = _zb_highlights(record, key)  # zero-based highlights
    rk = record[key]
    clusters = re.findall(r"[א-ת][^א-ת]*", rk)
    jc = "".join(clusters)
    assert jc == rk
    color = _RK_COLOR[key]
    out = [cl if i not in zbhls else _color(cl, color) for i, cl in enumerate(clusters)]
    return out


_RK_COLOR = {
    "bhla": "red",
    "mam": "green",
}
_RK_HL_SPECIFIC = {
    "bhla": "highlight-bhla",
    "mam": "highlight-mam",
}


def _color(text, color):
    return my_html.span(text, {"style": f"color: {color}"})


def _zb_highlights(record, key):
    hl_both = record.get("highlight")
    hl_spec = record.get(_RK_HL_SPECIFIC[key])
    assert (hl_both is None) or (hl_spec is None)
    hl = hl_both or hl_spec
    if isinstance(hl, int):
        return [hl - 1]
    assert isinstance(hl, list)
    return [obi - 1 for obi in hl]
