from temporal_normalization.rules.timespan_regex import CASE_INSENSITIVE

# -------------------------
# LONG DATE REGEX
# -------------------------

# Regex for structured long date format (s = second, a = year, l = month, z = day)
# Example format: s:12;a:2020;l:05;z:18

DATE_SEPARATOR = ";"

LONG_DATE_OPTIONS = (
        CASE_INSENSITIVE
        + "("
        + "^"
        + r"s:[\d]{1,2}"
        + DATE_SEPARATOR
        + r"a:[\d]{1,4}"
        + DATE_SEPARATOR
        + r"l:[\d]{1,2}"
        + DATE_SEPARATOR
        + r"z:[\d]{1,2}"
        + "$"
        + ")"
)

LONG_DATE_REGEXES = {
    LONG_DATE_OPTIONS
}
