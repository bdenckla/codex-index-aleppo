"""Exports gen_html_file"""

from pyauthor_util import author
from pyauthor_util.common_titles_etc import D5_TITLE, D5_H1_CONTENTS, D5_FNAME


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, D5_FNAME)
    cbody = _make_cbody()
    author.help_gen_html_file(tdm_ch, D5_FNAME, D5_TITLE, cbody)


def _make_cbody():
    return [
        author.heading_level_1(D5_H1_CONTENTS),
        author.para(_INTRO),
        author.heading_level_2("2 Samuel 18:20"),
        author.para(_SAMUEL_INTRO),
        author.blockquote(_SAMUEL_QUOTE, {"lang": "he"}),
        author.para(_SAMUEL_DISCUSSION),
        author.para_for_img("2-Samuel-c18v20.jpg"),
        author.heading_level_2("2 Kings 4:7"),
        author.para(_KINGS_INTRO),
        author.blockquote(_KINGS_QUOTE, {"lang": "he"}),
        author.para(_KINGS_DISCUSSION),
        author.para_for_img("2Kings-c4v7.png"),
        author.para_for_img("Aleppo-2Kings-c4v7.png"),
        author.heading_level_2("Lamentations 4:16"),
        author.para(_LAMENTATIONS_INTRO),
        author.blockquote(_LAMENTATIONS_QUOTE, {"lang": "he"}),
        author.para(_LAMENTATIONS_DISCUSSION),
        author.para_for_img("Sassoon-1053-Lamentations-c4v16.png"),
    ]


_INTRO = [
    "In the entry for Job 38:12 (the entry about the ה being copied rather than moved in the קרי),",
    " it is mentioned that a vowel mark floating before a כתיב word has manuscript precedent.",
    " This page presents some examples of that precedent.",
]

_SAMUEL_INTRO = [
    "2 Samuel 18:20 is a קרי ולא כתיב: the word ",
    author.hbo("כֵּ֥ן"),
    " is read but not written.",
    " In the Aleppo Codex, the Breuer edition notes:",
]
_SAMUEL_QUOTE = [
    [
        "אין רווח לתיבת ",
        author.hbo('\N{LEFT-TO-RIGHT MARK}"כֵּ֥ן"'),
        " הנקראת ולא נכתבת, אבל נכתבו הניקוד והטעם בין התיבות למטה",
    ],
]
_SAMUEL_DISCUSSION = [
    "I.e. there is no space for the word ",
    author.hbo("כֵּ֥ן"),
    " which is read but not written,",
    " but the pointing ($tsere) and accent ($merkha) were written between the words below.",
    " In other words, the vowel and accent marks of a קרי word",
    " float in the space between the surrounding כתיב words.",
]

_KINGS_INTRO = [
    "In 2 Kings 4:7, the כתיב of ",
    author.hbo("וּבָנַ֔יִךְ"),
    " is ",
    author.hbo("בֻ͏ָנַ֔יִכי"),
    ".",
    " The note in the Breuer edition of the Aleppo Codex says:",
]
_KINGS_QUOTE = [
    'נקודות הקובוץ עוד לפני האות בי"ת מימין למטה, ואין שווא במקביל לקרי',
]
_KINGS_DISCUSSION = [
    "I.e. the $qamats dots (of the קבוץ) are placed even before the letter בית,",
    " to the right below,",
    " and there is no $shewa corresponding to the קרי.",
    " This is a direct parallel:",
    " a vowel mark floating before its expected letter in a כתיב word in the Aleppo Codex.",
    " The first image below is from μL; the second is from μA.",
]

_LAMENTATIONS_INTRO = [
    "In Lamentations 4:16, the כתיב of ",
    author.hbo("וּזְקֵנִ֖ים"),
    " is ",
    author.hbo("זְקֵנִ֖ים"),
    ".",
    " The note in the Breuer edition of the Aleppo Codex says:",
]
_LAMENTATIONS_QUOTE = [
    'חסרות שלושת הנקודות של שורוק לפני האות זי"ן',
]
_LAMENTATIONS_DISCUSSION = [
    "I.e. the three dots of the $shuruq are missing before the letter זין.",
    " However, another manuscript (Sassoon 1053) has ",
    author.hbo("ֻזְקֵנִ֖ים"),
    " — with a קבוץ floating in the space before the word.",
    " This is another example of a vowel mark floating before a כתיב word.",
]
