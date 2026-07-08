from temporal_normalization.rules.date.date_regex import (
    DATE_DMY_OPTIONS,
    DATE_YMD_OPTIONS,
)

from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    REGEX_INTERVAL_DELIMITER,
    REGEX_PUNCTUATION_UNLIMITED,
    TEXT_START,
    TEXT_END,
)

from temporal_normalization.rules.year.year_regex import (
    YEAR_NOTATION
)

# -------------------------
# INACCURATE YEAR REGEX
# -------------------------

"""
Approximation notation for uncertain years.
"""
APPROX_NOTATION_ITEMS = [
    r"catre",
    r"probabil",
    r"aprox[\.]*",
    r"aproximativ(\s*anii)?",
    r"cca[\.]*",
    r"c[a]?[\.]?",
    r"circa"
]
APPROX_NOTATION = TEXT_START + "(" + "|".join(APPROX_NOTATION_ITEMS) + r")\s*"


APPROX_AGES_GROUP = (
        "("
        + "(" + APPROX_NOTATION + r"\d+" + ")"
        + "(" + REGEX_PUNCTUATION_UNLIMITED + AD_BC_OPTIONAL + ")*"
        + ")"
)

APPROX_AGES_OPTIONS = TEXT_START + APPROX_AGES_GROUP + TEXT_END


APPROX_AGES_INTERVAL_1 = (
        TEXT_START
        + APPROX_AGES_GROUP
        + REGEX_INTERVAL_DELIMITER
        + "("
        + APPROX_AGES_GROUP + "|" + "(" + YEAR_NOTATION + ")"
        + ")"
        + TEXT_END
)

# E.g.: "281 a.chr. - cca 200 a.chr."
APPROX_AGES_INTERVAL_2 = (
        TEXT_START
        + "(" + YEAR_NOTATION + ")"
        + REGEX_INTERVAL_DELIMITER
        + "(" + APPROX_AGES_GROUP + ")"
        + TEXT_END
)

APPROX_AGES_INTERVAL = APPROX_AGES_INTERVAL_1 + "|" + APPROX_AGES_INTERVAL_2


DATE = (
        "("
        + DATE_DMY_OPTIONS + "|"
        + DATE_YMD_OPTIONS + "|"
        + "(" + TEXT_START + r"\d{1,4}" + AD_BC_OPTIONAL + TEXT_END + ")"
        + ")"
)

"""
E.g.:
    - "după 1628"
    - "dupa 29 aprilie 1616"
    - "post 330-320 a.chr."
    - "postum 161 p.chr."
"""
AFTER = TEXT_START + r"(dupa|post|postum)\s*" + DATE + TEXT_END
AFTER_INTERVAL = AFTER + REGEX_INTERVAL_DELIMITER + DATE


"""
E.g.:
    - "ante 1801"
    - "anterior lui 1890 (data mortii mesterului)"
    - "inainte de 211 a.chr."
"""
BEFORE = TEXT_START + r"(ante|anterior\s*lui|inainte\s*de)\s*" + DATE + TEXT_END
BEFORE_INTERVAL = BEFORE + REGEX_INTERVAL_DELIMITER + DATE


INACCURATE_YEAR_REGEXES = {
    AFTER,
    AFTER_INTERVAL,
    APPROX_AGES_GROUP,
    APPROX_AGES_INTERVAL,
    APPROX_AGES_OPTIONS,
    BEFORE,
    BEFORE_INTERVAL,
}
