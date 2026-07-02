from temporal_normalization.rules.date.date_regex import (
    DATE_DMY_OPTIONS,
    DATE_YMD_OPTIONS,
)

from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    REGEX_INTERVAL_DELIMITER,
    REGEX_OR,
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
APPROX_NOTATION = (
        TEXT_START
        + "("
        + "catre" + REGEX_OR
        + "probabil" + REGEX_OR
        + r"aprox[\.]*" + REGEX_OR
        + r"aproximativ(\s*anii)?" + REGEX_OR
        + r"cca[\.]*" + REGEX_OR
        + r"c[a]?[\.]?" + REGEX_OR
        + "circa"
        + r")\s*"
)


APPROX_AGES_GROUP = (
        "("
        + "("
        + APPROX_NOTATION + r"\d+"
        + ")"
        + "(" + REGEX_PUNCTUATION_UNLIMITED + AD_BC_OPTIONAL + ")*"
        + ")"
)

APPROX_AGES_OPTIONS = TEXT_START + APPROX_AGES_GROUP + TEXT_END


APPROX_AGES_INTERVAL_1 = (
        TEXT_START
        + APPROX_AGES_GROUP
        + REGEX_INTERVAL_DELIMITER
        + "("
        + APPROX_AGES_GROUP + REGEX_OR
        + "(" + YEAR_NOTATION + ")"
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

APPROX_AGES_INTERVAL = (
        APPROX_AGES_INTERVAL_1
        + REGEX_OR
        + APPROX_AGES_INTERVAL_2
)


DATE = (
        "("
        + DATE_DMY_OPTIONS + REGEX_OR
        + DATE_YMD_OPTIONS + REGEX_OR
        + "("
        + TEXT_START + r"\d{1,4}" + AD_BC_OPTIONAL + TEXT_END
        + ")"
        + ")"
)

"""
E.g.:
<ul>
    <li>"după 1628"</li>
    <li>"dupa 29 aprilie 1616"</li>
    <li>"post 330-320 a.chr."</li>
    <li>"postum 161 p.chr."</li>
</ul>
"""
AFTER = (
        TEXT_START
        + "("
        + "("
        + "dupa" + REGEX_OR
        + "post" + REGEX_OR
        + "postum"
        + r")\s*"
        + DATE
        + ")"
        + TEXT_END
)

AFTER_INTERVAL = AFTER + REGEX_INTERVAL_DELIMITER + DATE


"""
E.g.:
<ul>
    <li>"ante 1801"</li>
    <li>"anterior lui 1890 (data mortii mesterului)"</li>
    <li>"inainte de 211 a.chr."</li>
</ul>
"""
BEFORE = (
        TEXT_START
        + "("
        + "("
        + "ante" + REGEX_OR
        + r"anterior\s*lui" + REGEX_OR
        + r"inainte\s*de"
        + r")\s*"
        + DATE
        + ")"
        + TEXT_END
)

# FIXME: "înainte de 01.01.1911 - 01.01.1914"
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
