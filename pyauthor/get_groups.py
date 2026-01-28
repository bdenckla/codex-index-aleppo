from .job2_main_article import _nbhq_and_ne, _nbhq_and_xe, _tbhq_and_ne, _tbhq_and_zwd, _tbhq_and_zwm, _xbhq_and_ne


def get_groups(quirkrecs):
    # nbhq, xbhq: noted (as a quirk) in BHQ, not noted (as a quirk) in BHQ
    # ne, xe: noted (as a quirk) elsewhere, not noted (as a quirk) elsewhere
    # zw (zWLCmisc): noted (as consensus) by WLC (combined with MAM):
    #     flagged as a change in WLC relative to BHS, e.g. a bracket-c or bracket-v note.
    #     comparison with MAM revealed that it is a change back towards consensus,
    #     i.e. this is BHS/BHQ proposing a quirk that is not in μL
    q_nbhq_and_xe = list(filter(_nbhq_and_xe, quirkrecs))
    q_nbhq_and_ne = list(filter(_nbhq_and_ne, quirkrecs))
    q_xbhq_and_ne = list(filter(_xbhq_and_ne, quirkrecs))
    q_tbhq_and_ne = list(filter(_tbhq_and_ne, quirkrecs))
    q_tbhq_and_zwm = list(filter(_tbhq_and_zwm, quirkrecs))
    q_tbhq_and_zwd = list(filter(_tbhq_and_zwd, quirkrecs))
    groups = [
        q_nbhq_and_xe,
        q_nbhq_and_ne,
        q_xbhq_and_ne,
        q_tbhq_and_ne,
        q_tbhq_and_zwd,
        q_tbhq_and_zwm,
    ]
    return groups