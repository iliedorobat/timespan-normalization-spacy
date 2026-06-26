from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    CASE_INSENSITIVE,
    FIRST_HALF,
    FIRST_QUARTER,
    FORTH_QUARTER,
    MIDDLE_OF,
    MONTHS,
    REGEX_INTERVAL_CONJUNCTION,
    REGEX_INTERVAL_DELIMITER,
    REGEX_INTERVAL_PREFIX,
    REGEX_OR,
    REGEX_PUNCTUATION_UNLIMITED,
    SECOND_HALF,
    SECOND_QUARTER,
    TEXT_START,
    TEXT_END,
    THIRD_QUARTER,
    YEAR_LABEL,
)

# -------------------------
# YEAR REGEX
# -------------------------

BRACKETS_START = r"[\[\(]"
BRACKETS_END = r"[\]\)]"


PREFIX_CONSTRUCTIONS = (
        "lunile" + REGEX_OR + "luni(i|[aă]|lor)?" + REGEX_OR + "lun[ăa]" + REGEX_OR
        + r"s[ăa]pt[ăa]m[âa]ni(i|le|lor)?" + REGEX_OR + r"s[ăa]pt[ăa]m[âa]n[ăa]" + REGEX_OR
        + "zile(le|lor)?" + REGEX_OR + "ziu[ăa]" + REGEX_OR + "zi" + REGEX_OR
        + "ore(i|le|lor)?" + REGEX_OR + "or[ăa]" + REGEX_OR
        + "minute(le|lor)?" + REGEX_OR + r"minut(ului|ul)?" + REGEX_OR
        + "secunde(i|le|lor)?" + REGEX_OR + r"secund[ăa]" + REGEX_OR
        + "milisecunde(i|le|lor)?" + REGEX_OR + r"milisecund[ăa]"
)

POSTFIX_CONSTRUCTIONS = (
        r"ani(lor)?" + REGEX_OR
        + r"an(ului|ul)?" + REGEX_OR
        + PREFIX_CONSTRUCTIONS
)

# Prevents matching patterns like "luna 38", "ziua 10", etc.
EXCLUDED_PREFIX = rf"(?<!(?:{PREFIX_CONSTRUCTIONS})\s)"

# Prevents matching patterns like "38 de ani", "38 ani", etc.
EXCLUDED_POSTFIX = rf"(?!\s*(?:de\s*)?(?:{POSTFIX_CONSTRUCTIONS}))"


# TODO: verify if the removal of capturing the group generates bugs: r'(\s*(?:/|sau)\s*)'
YEAR_OR_SEPARATOR = r'\s*(?:/|sau)\s*'

# E.g.: "15.000"; "[1]989"; "(19)89"; "1989"; "(19)89 martie"
YEAR_GROUP_1 = (
        "(?:"
        + r"\d{1,3}\.(?:\d{3}\.?)+"
        + REGEX_OR
        + BRACKETS_START + r"\d{1,4}" + BRACKETS_END + r"\d{0,3}"
        + REGEX_OR
        + r"\d?" + BRACKETS_START + r"\d{1,3}" + BRACKETS_END + r"\d{0,2}"
        + REGEX_OR
        + r"\d{3,4}"
        + ")"
        + MONTHS
        + "?"
)

# Prevents matching day-month expressions like "23 martie" and hour-minutes expressions like "18.05"
YEAR_GROUP_2 = r"(?:\d{2,3})" + rf"(?!({MONTHS})|(\.\d))\b"

YEAR_GROUP = rf"(?<![\d\.])({YEAR_GROUP_1}|{YEAR_GROUP_2}){EXCLUDED_POSTFIX}"

YEAR_NOTATION = EXCLUDED_PREFIX + YEAR_GROUP + AD_BC_OPTIONAL


YEAR = (
        CASE_INSENSITIVE
        + "("
        # + TEXT_START
        + "(" + YEAR_LABEL + ")?"
        + YEAR_NOTATION
        # + TEXT_END
        + ")"
)

YEAR_FIRST_HALF = FIRST_HALF + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_SECOND_HALF = SECOND_HALF + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_MIDDLE_OF = MIDDLE_OF + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_FIRST_QUARTER = FIRST_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_SECOND_QUARTER = SECOND_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_THIRD_QUARTER = THIRD_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR
YEAR_FORTH_QUARTER = FORTH_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR


YEAR_OPTIONS = (
        CASE_INSENSITIVE
        + "("
        + "(" + YEAR_FIRST_HALF + ")" + REGEX_OR
        + "(" + YEAR_SECOND_HALF + ")" + REGEX_OR
        + "(" + YEAR_MIDDLE_OF + ")" + REGEX_OR
        + "(" + YEAR_FIRST_QUARTER + ")" + REGEX_OR
        + "(" + YEAR_SECOND_QUARTER + ")" + REGEX_OR
        + "(" + YEAR_THIRD_QUARTER + ")" + REGEX_OR
        + "(" + YEAR_FORTH_QUARTER + ")" + REGEX_OR
        + "(" + YEAR + ")"
        + ")"
)


YEAR_INTERVAL_BASE = (
        CASE_INSENSITIVE
        + TEXT_START
        + "("
        + YEAR_OPTIONS
        + REGEX_INTERVAL_DELIMITER
        + YEAR_OPTIONS
        + ")"
)

YEAR_INTERVAL_PREFIXED = (
        CASE_INSENSITIVE
        + TEXT_START
        + "("
        + REGEX_INTERVAL_PREFIX
        + YEAR_OPTIONS
        + REGEX_INTERVAL_CONJUNCTION
        + YEAR_OPTIONS
        + ")"
)


YEAR_3_4_DIGITS_SPECIAL_PREFIX = r"(anul\s*\d{1,2}=)"


# "anul 13=1800/1801"; "110/109 a. chr."; "112 sau 111 î.chr."
YEAR_3_4_DIGITS_SPECIAL_INTERVAL = (
        CASE_INSENSITIVE
        + TEXT_START
        + "("
        + r"\d{3,4}" + AD_BC_OPTIONAL
        + YEAR_OR_SEPARATOR
        + r"\d{3,4}" + AD_BC_OPTIONAL
        + ")"
        + TEXT_END
)


# "(1)838"; "15(6)3"; "173[1]"; "184(5)"; "1700(?!)"; "(15…)"
UNKNOWN_YEARS = (
        "("
        + "(" + r"[\[\(\]\)\?\!\d\…]{5,}" + ")"
        + ")"
)


YEAR_REGEXES = {
    YEAR_INTERVAL_BASE,
    YEAR_INTERVAL_PREFIXED,
    YEAR_3_4_DIGITS_SPECIAL_INTERVAL,
    YEAR_OPTIONS,
}
