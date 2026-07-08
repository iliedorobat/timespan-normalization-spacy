from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    MONTHS,
    REGEX_INTERVAL_DELIMITER,
)

# Regular expressions for those time intervals that are stored
# as a date (having a year, a month and a day)

# -------------------------
# DATE DMY (day-month-year)
# -------------------------

# d{3,} allows avoiding the month-day pattern (E.g.: "noiembrie 22")
DATE_DMY_DOT = r"\d{1,2}\.\d{1,2}\.\d{3,}"  # E.g.: "01.01.1911"
DATE_DMY_SLASH = r"\d{1,2}\/\d{2}\/\d{3,}"  # E.g.: "21/01/1916"
DATE_DMY_SPACE = r"\d{1,2}\s+\d{2}\s+\d{3,}"  # E.g.: "7 06 1911"
DATE_DMY_TEXT = rf"\d{{1,2}}[,\s]+{MONTHS}[,\s]+\d{{3,}}"  # E.g.: "9 iulie 1807"

DATE_DMY_ITEMS = [
    DATE_DMY_DOT,
    DATE_DMY_SLASH,
    DATE_DMY_SPACE,
    DATE_DMY_TEXT,
]

DATE_DMY_BASE_OPTIONS = "|".join(DATE_DMY_ITEMS)

DATE_DMY_OPTIONS = (
        "(" + DATE_DMY_BASE_OPTIONS + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# PARTIAL DMY (day-month-year)
# -------------------------

DATE_DMY_DOT_PARTIAL = r"\d{1,2}\.\d{2}" + r"(\.\d{3,})?"
DATE_DMY_SLASH_PARTIAL = r"\d{1,2}\/\d{2}" + r"(\/\d{3,})?"
DATE_DMY_SPACE_PARTIAL = r"\d{1,2}\s+\d{2}" + r"(\s+\d{3,})?"
DATE_DMY_TEXT_PARTIAL = rf"\d{{1,2}}[, ]+{MONTHS}([,\s]+\d{{3,}})?"  # E.g.: "10 iunie - 15 octombrie 1382"

DATE_DMY_PARTIAL_ITEMS = [
    DATE_DMY_DOT_PARTIAL,
    DATE_DMY_SLASH_PARTIAL,
    DATE_DMY_SPACE_PARTIAL,
    DATE_DMY_TEXT_PARTIAL,
]

DATE_DMY_PARTIAL_BASE_OPTIONS = "|".join(DATE_DMY_PARTIAL_ITEMS)

DATE_DMY_PARTIAL_OPTIONS = (
        "(" + DATE_DMY_PARTIAL_BASE_OPTIONS + "|" + r"\d{1,2}\s*" + MONTHS + r"?" + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# DATE YMD (year-month-day)
# -------------------------

DATE_YMD_DASH = r"\d{3,}[-]{1}\d{2}[-]{1}\d{1,2}"  # E.g.: "1698-10-15"
DATE_YMD_TEXT = rf"\d{{3,}}[,\s]+{MONTHS}[,\s]+\d{{1,2}}"  # E.g.: "1752 aprilie 25"

DATE_YMD_ITEMS = [
    DATE_YMD_DASH,
    DATE_YMD_TEXT,
]

DATE_YMD_BASE_OPTIONS = "|".join(DATE_YMD_ITEMS)

DATE_YMD_OPTIONS = (
        "(" + DATE_YMD_BASE_OPTIONS + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# INTERVAL REGEX
# -------------------------

DATE_DMY_INTERVAL = DATE_DMY_OPTIONS + REGEX_INTERVAL_DELIMITER + DATE_DMY_OPTIONS
DATE_DMY_INTERVAL_PARTIAL = DATE_DMY_PARTIAL_OPTIONS + REGEX_INTERVAL_DELIMITER + DATE_DMY_OPTIONS
DATE_YMD_INTERVAL = DATE_YMD_OPTIONS + REGEX_INTERVAL_DELIMITER + DATE_YMD_OPTIONS


DATE_DMY_REGEXES = [
    DATE_DMY_INTERVAL,
    DATE_DMY_INTERVAL_PARTIAL,
    DATE_DMY_OPTIONS,
]

DATE_YMD_REGEXES = [
    DATE_YMD_INTERVAL,
    DATE_YMD_OPTIONS,
]
