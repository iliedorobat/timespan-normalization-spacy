from temporal_normalization.rules.timespan_regex import (
    AD_BC_OPTIONAL,
    FIRST_HALF,
    FIRST_QUARTER,
    FORTH_QUARTER,
    MIDDLE_OF,
    MONTHS,
    REGEX_INTERVAL_CONJUNCTION,
    REGEX_INTERVAL_DELIMITER,
    REGEX_INTERVAL_PREFIX,
    REGEX_PUNCTUATION_UNLIMITED,
    SECOND_HALF,
    SECOND_QUARTER,
    TEXT_START,
    TEXT_END,
    THIRD_QUARTER,
    YEAR_LABEL,
)


BRACKETS_START = r"[\[\(]"
BRACKETS_END = r"[\]\)]"

PREFIX_ITEMS = [
    r"lunile",
    r"luni(i|[aă]|lor)?",
    r"lun[ăa]",
    r"s[ăa]pt[ăa]m[âa]ni(i|le|lor)?",
    r"s[ăa]pt[ăa]m[âa]n[ăa]",
    r"zile(le|lor)?",
    r"ziu[ăa]",
    r"zi",
    r"ore(i|le|lor)?",
    r"or[ăa]",
    r"minute(le|lor)?",
    r"minut(ului|ul)?",
    r"secunde(i|le|lor)?",
    r"secund[ăa]",
    r"milisecunde(i|le|lor)?",
    r"milisecund[ăa]",
]

PREFIX_CONSTRUCTIONS = "|".join(PREFIX_ITEMS)
POSTFIX_CONSTRUCTIONS = r"ani(lor)?" + "|" + r"an(ului|ul)?" + "|" + PREFIX_CONSTRUCTIONS

# Prevents matching patterns like "luna 38", "ziua 10", etc.
EXCLUDED_PREFIX = rf"(?<!(?:{PREFIX_CONSTRUCTIONS})\s)"

# Prevents matching patterns like "38 de ani", "38 ani", etc.
EXCLUDED_POSTFIX = rf"(?!\s*(?:de\s*)?(?:{POSTFIX_CONSTRUCTIONS}))"

YEAR_OR_SEPARATOR = r'\s*(?:/|sau)\s*'

# E.g.: "15.000"; "[1]989"; "(19)89"; "1989"; "(19)89 martie"
YEAR_GROUP_1 = (
        "(?:"
        + r"\d{1,3}\.(?:\d{3}\.?)+"
        + "|"
        + BRACKETS_START + r"\d{1,4}" + BRACKETS_END + r"\d{0,3}"
        + "|"
        + r"\d?" + BRACKETS_START + r"\d{1,3}" + BRACKETS_END + r"\d{0,2}"
        + "|"
        + r"\d{3,4}"
        + ")"
        + MONTHS
        + "?"
)

# Prevents matching day-month expressions like "23 martie" and hour-minutes expressions like "18.05"
YEAR_GROUP_2 = r"(?<!\d)" + r"(?:\d{2,3})" + rf"(?!\s*(?:{MONTHS})|\.\d)" + r"\b"

YEAR_GROUP = rf"(?<![\d\.])({YEAR_GROUP_1}|{YEAR_GROUP_2}){EXCLUDED_POSTFIX}"

YEAR_NOTATION = EXCLUDED_PREFIX + YEAR_GROUP + AD_BC_OPTIONAL

YEAR = TEXT_START + "(" + YEAR_LABEL + ")?" + YEAR_NOTATION + TEXT_END

YEAR_ITEMS = [
    FIRST_HALF + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    SECOND_HALF + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    MIDDLE_OF + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    FIRST_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    SECOND_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    THIRD_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    FORTH_QUARTER + REGEX_PUNCTUATION_UNLIMITED + YEAR,
    YEAR,
]

YEAR_OPTIONS = "(" + "|".join(f"({pattern})" for pattern in YEAR_ITEMS) + ")"

YEAR_INTERVAL_BASE = (
        TEXT_START
        + "(" + YEAR_OPTIONS + REGEX_INTERVAL_DELIMITER + YEAR_OPTIONS + ")"
)

YEAR_INTERVAL_PREFIXED = (
        TEXT_START
        + "("
        + REGEX_INTERVAL_PREFIX + YEAR_OPTIONS + REGEX_INTERVAL_CONJUNCTION + YEAR_OPTIONS
        + ")"
)

YEAR_3_4_DIGITS_SPECIAL_PREFIX = r"(anul\s*\d{1,2}=)"

# "anul 13=1800/1801"; "110/109 a. chr."; "112 sau 111 î.chr."
YEAR_3_4_DIGITS_SPECIAL_INTERVAL = (
        TEXT_START
        + "("
        + r"\d{3,4}" + AD_BC_OPTIONAL + YEAR_OR_SEPARATOR + r"\d{3,4}" + AD_BC_OPTIONAL
        + ")"
        + TEXT_END
)

# "(1)838"; "15(6)3"; "173[1]"; "184(5)"; "1700(?!)"; "(15…)"
UNKNOWN_YEARS = r"[\[\(\]\)\?\!\d\…]{5,}"

YEAR_REGEXES = [
    YEAR_INTERVAL_BASE,
    YEAR_INTERVAL_PREFIXED,
    YEAR_3_4_DIGITS_SPECIAL_INTERVAL,
    YEAR_OPTIONS,
]
