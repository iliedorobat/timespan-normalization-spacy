from temporal_normalization.rules import UNKNOWN
from temporal_normalization.rules.timespan_regex import (
    REGEX_OR,
    TEXT_START,
    TEXT_END,
    CASE_INSENSITIVE,
)
from temporal_normalization.rules.year import UNKNOWN_YEARS

# -------------------------
# IMPLICIT DATELESS REGEXES
# -------------------------

"""
E.g.:
<ul>
    <li>"model 1850"</li>
</ul>
"""
MODEL_X = rf"({TEXT_START}model\s*\d{{4}}){TEXT_END}"


"""
E.g.:
<ul>
    <li>"nedatat (1897)"</li>
    <li>"1910 (nedatat)"</li>
    <li>"nedatabil"</li>
    <li>"nu are"</li>
</ul>
"""
UNDATED = rf"(" \
          rf".*(" \
          rf"nedatat{REGEX_OR}" \
          rf"nedatabil{REGEX_OR}" \
          r"nu\s*are" \
          rf").*" \
          rf")"


"""
E.g.:
<ul>
    <li>"f.a. octombrie 29"; "f.an"</li>
</ul>
"""
WITHOUT_AGE = rf"(" \
              rf".*(" \
              rf"(fara\s*an){REGEX_OR}" \
              rf"(f\.\s*an){REGEX_OR}" \
              r"(f\.a)" \
              rf")" \
              rf")"


"""
E.g.:
<ul>
    <li>"fara data"</li>
    <li>"1861 f.d"</li>
</ul>
"""
WITHOUT_DATE = rf"(" \
               rf"(" \
               rf"(fara\s*data){REGEX_OR}" \
               rf"(f\.\s*data){REGEX_OR}" \
               r"(f\.d)" \
               rf")" \
               rf").*"


"""
E.g.:
<ul>
    <li>"f.a. octombrie 29"; "f.an"</li>
    <li>"fara data"</li>
    <li>"1861 f.d"</li>
</ul>
"""
DATELESS = (
        CASE_INSENSITIVE
        + "("
        + WITHOUT_AGE
        + REGEX_OR
        + WITHOUT_DATE
        + ")"
)


"""
E.g.:
<ul>
    <li>"model 1850"</li>
</ul>
"""
DATELESS_MODEL_X = CASE_INSENSITIVE + MODEL_X


"""
E.g.:
<ul>
    <li>"nedatat (1897)"</li>
    <li>"1910 (nedatat)"</li>
    <li>"nedatabil"</li>
    <li>"nu are"</li>
</ul>
"""
DATELESS_UNDATED = CASE_INSENSITIVE + UNDATED


DATELESS_REGEXES = {
    DATELESS,
    DATELESS_MODEL_X,
    DATELESS_UNDATED,
    UNKNOWN_YEARS,
    UNKNOWN,
}
