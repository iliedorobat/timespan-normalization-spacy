from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    MONTHS,
    REGEX_INTERVAL_DELIMITER,
    REGEX_OR,
    TEXT_START,
    TEXT_END,
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

DATE_DMY = (
        "("
        + DATE_DMY_DOT + REGEX_OR
        + DATE_DMY_SLASH + REGEX_OR
        + DATE_DMY_SPACE + REGEX_OR
        + DATE_DMY_TEXT
        + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# PARTIAL DMY
# -------------------------

DATE_DMY_DOT_PARTIAL = r"\d{1,2}\.\d{2}" + r"(\.\d{3,})?"
DATE_DMY_SLASH_PARTIAL = r"\d{1,2}\/\d{2}" + r"(\/\d{3,})?"
DATE_DMY_SPACE_PARTIAL = r"\d{1,2}\s+\d{2}" + r"(\s+\d{3,})?"
DATE_DMY_TEXT_PARTIAL = rf"\d{{1,2}}[, ]+{MONTHS}([,\s]+\d{{3,}})?"  # E.g.: "10 iunie - 15 octombrie 1382"

DATE_DMY_PARTIAL = (
        "("
        + DATE_DMY_DOT_PARTIAL + REGEX_OR
        + DATE_DMY_SLASH_PARTIAL + REGEX_OR
        + DATE_DMY_SPACE_PARTIAL + REGEX_OR
        + DATE_DMY_TEXT_PARTIAL + REGEX_OR
        + r"\d{1,2}\s*" + MONTHS + r"?"
        + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# DATE YMD (year-month-day)
# -------------------------

DATE_YMD_DASH = r"\d{3,}[-]{1}\d{2}[-]{1}\d{1,2}"  # E.g.: "1698-10-15"
DATE_YMD_TEXT = rf"\d{{3,}}[,\s]+{MONTHS}[,\s]+\d{{1,2}}"  # E.g.: "1752 aprilie 25"

DATE_YMD = (
        "(" + DATE_YMD_DASH + REGEX_OR + DATE_YMD_TEXT + ")"
        + AD_BC_OPTIONAL
)

# -------------------------
# INTERVAL START / END
# -------------------------

DATE_DMY_INTERVAL_START = TEXT_START + DATE_DMY_PARTIAL
DATE_YMD_INTERVAL_START = TEXT_START + DATE_YMD

DATE_DMY_INTERVAL_END = DATE_DMY + TEXT_END
DATE_YMD_INTERVAL_END = DATE_YMD + TEXT_END

# -------------------------
# INTERVAL REGEX
# -------------------------

DATE_DMY_INTERVAL = DATE_DMY_INTERVAL_START + REGEX_INTERVAL_DELIMITER + DATE_DMY_INTERVAL_END
DATE_YMD_INTERVAL = DATE_YMD_INTERVAL_START + REGEX_INTERVAL_DELIMITER + DATE_YMD_INTERVAL_END

# -------------------------
# OPTIONS
# -------------------------

DATE_DMY_OPTIONS = TEXT_START + DATE_DMY + TEXT_END
DATE_YMD_OPTIONS = TEXT_START + DATE_YMD + TEXT_END


DATE_YMD_REGEXES = {
    DATE_YMD_INTERVAL,
    DATE_YMD_OPTIONS,
}

DATE_DMY_REGEXES = {
    DATE_DMY_INTERVAL,
    DATE_DMY_OPTIONS,
}
