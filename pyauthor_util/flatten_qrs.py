from pycmn.shrink import shrink
from py import my_html


def _enrich_one_qr_by_flattening_strs(quirkrec):
    wiw = quirkrec["qr-what-is-weird"]
    gencom = quirkrec.get("qr-generic-comment")
    bhqcom = quirkrec.get("qr-bhq-comment")
    flat_wiw = _flatten_yyycom(wiw)
    flat_gencom = gencom and _flatten_yyycom(gencom)
    flat_bhqcom = bhqcom and _flatten_yyycom(bhqcom)
    new_wiw = {"qr-what-is-weird": flat_wiw} if flat_wiw else {}
    new_gencom = {"qr-generic-comment": flat_gencom} if flat_gencom else {}
    new_bhqcom = {"qr-bhq-comment": flat_bhqcom} if flat_bhqcom else {}
    return {**quirkrec, **new_wiw, **new_gencom, **new_bhqcom}


def _flatten_yyycom(yyycom):
    if isinstance(yyycom, str):
        return yyycom
    assert isinstance(yyycom, list)
    flat = my_html.flatten(yyycom)
    return shrink(flat)
