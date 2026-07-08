from temporal_normalization.rules import UNKNOWN_REGEXES
from temporal_normalization.rules.timespan_regex import (
    TEXT_START,
    TEXT_END,
)
from temporal_normalization.rules.year import UNKNOWN_YEARS


"""
E.g.:
    - "f.a. octombrie 29"; "f.an"
"""
WITHOUT_AGE = rf"(.*((fara\s*an)|(f\.\s*an)|(f\.a)))"


"""
E.g.:
    - "fara data"
    - "1861 f.d"
"""
WITHOUT_DATE = rf"(((fara\s*data)|(f\.\s*data)|(f\.d))).*"


"""
E.g.:
    - "f.a. octombrie 29"; "f.an"
    - "fara data"
    - "1861 f.d"
"""
DATELESS = "(" + WITHOUT_AGE + "|" + WITHOUT_DATE + ")"


"""
E.g.:
    - "model 1850"
"""
DATELESS_MODEL_X = rf"({TEXT_START}model\s*\d{{4}}){TEXT_END}"


"""
E.g.:
    - "nedatat (1897)"
    - "1910 (nedatat)"
    - "nedatabil"
    - "nu are"
"""
DATELESS_UNDATED = rf"(.*(nedatat|nedatabil|nu\s*are).*)"


DATELESS_REGEXES = [
    DATELESS,
    DATELESS_MODEL_X,
    DATELESS_UNDATED,
    UNKNOWN_YEARS,
    UNKNOWN_REGEXES,
]
