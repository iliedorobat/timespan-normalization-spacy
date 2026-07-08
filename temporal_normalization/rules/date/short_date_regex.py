from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    MONTHS,
    REGEX_INTERVAL_DELIMITER,
    TEXT_END,
    TEXT_START,
)

"""
Regular expressions for those time intervals that are stored
as a date (having just a year and a month)
"""

# -------------------------
# SHORT DATE REGEX
# -------------------------

# d{3,} allows us to avoid the month-day pattern (E.g.: "noiembrie 22")
SHORT_DATE_MY_TEXT = rf"({MONTHS}\s+\d{{3,}})"

SPECIAL_YEAR_NOTATION = r"\s*[\(\[]?\d+[\)\]]?\s*"


DATE_MY_INTERVAL = (
        # Avoid match intervals consisting only of years (E.g.: "1789 - 1797")
        rf"^(?!{SPECIAL_YEAR_NOTATION}{REGEX_INTERVAL_DELIMITER}{SPECIAL_YEAR_NOTATION}$).*"
        + TEXT_START

        # E.g.: noiembrie 1784 - aprilie 1785
        + "("
        + "(" + SHORT_DATE_MY_TEXT + AD_BC_OPTIONAL + ")"
        + REGEX_INTERVAL_DELIMITER
        + "(" + SHORT_DATE_MY_TEXT + AD_BC_OPTIONAL + ")"
        + ")"

        + "|"

        # E.g.: noiembrie 1784 - 1785
        + "("
        + SHORT_DATE_MY_TEXT + AD_BC_OPTIONAL
        + REGEX_INTERVAL_DELIMITER
        + "(" + SHORT_DATE_MY_TEXT + "|" + r"\d{3,}" + ")" + AD_BC_OPTIONAL
        + ")"

        + "|"

        # E.g.: 1784 - aprilie 1785
        + "("
        + "(" + SHORT_DATE_MY_TEXT + "|" + r"\d{3,}" + ")" + AD_BC_OPTIONAL
        + REGEX_INTERVAL_DELIMITER
        + SHORT_DATE_MY_TEXT + AD_BC_OPTIONAL
        + ")"

        + TEXT_END
)


DATE_MY_OPTIONS = MONTHS + r"\s+\d{3,}" + AD_BC_OPTIONAL


DATE_MY_REGEXES = [
    DATE_MY_INTERVAL,
    DATE_MY_OPTIONS,
]
