import re

import regex

from temporal_normalization.commons_temporal import (
    CHRISTUM_AD_PLACEHOLDER,
    clear_christum_notation,
    clear_date,
    EMPTY_VALUE_PLACEHOLDER,
    roman_to_int,
)
from temporal_normalization.rules import (
    AGES_GROUP_SUFFIX,
    ARTICLE_AL,
    CENTURY_LABEL,
    FIRST_HALF,
    FIRST_QUARTER,
    FORTH_QUARTER,
    MIDDLE_OF,
    MILLENNIUM_LABEL,
    REGEX_INTERVAL_PREFIX,
    REGEX_INTERVAL_CONJUNCTION,
    SECOND_QUARTER,
    SECOND_HALF,
    START_END,
    THIRD_QUARTER,
    YEAR_LABEL,
)

SPECIAL_CHARS_REGEX = r"[\.,;\?!]*\s*"

REGEX_LIST = [
    START_END,
    FIRST_HALF,
    SECOND_HALF,
    MIDDLE_OF,
    FIRST_QUARTER,
    SECOND_QUARTER,
    THIRD_QUARTER,
    FORTH_QUARTER,
    CENTURY_LABEL,
    MILLENNIUM_LABEL,
    YEAR_LABEL,
    AGES_GROUP_SUFFIX,
    ARTICLE_AL,
    SPECIAL_CHARS_REGEX,
]

# =========================================================
# Get the time period value from the input value
# @param value The initial value
# @return The prepared value (E.g.: i, ii, iii, iv etc.)
# =========================================================


def sanitize_time_period(value: str) -> str:
    prepared_value = value
    groups = _get_group_list(prepared_value)

    for group in reversed(groups):
        if not group:
            continue

        # E.g.: "3/4. sec. 19", "4/4. xviii - 1/4. xix", "sf sec.xix - mijl. sec. xx"
        if _special_chars_only(group) and "." in group:
            group = group.replace(".", "")
            prepared_value = prepared_value.replace(".", EMPTY_VALUE_PLACEHOLDER)

        prepared_value = prepared_value.replace(group, EMPTY_VALUE_PLACEHOLDER)

    prepared_value = re.sub(r"\s*", EMPTY_VALUE_PLACEHOLDER, prepared_value)

    return prepared_value


# TODO: add documentation
def sanitize_time_period_interval(value: str) -> str:
    prepared_value = (
        regex.sub(REGEX_INTERVAL_PREFIX, "", value, flags=regex.IGNORECASE)
    )
    prepared_value = (
        regex.sub(REGEX_INTERVAL_CONJUNCTION, " - ", prepared_value, flags=regex.IGNORECASE)
    )
    return sanitize_time_period(prepared_value.strip())

# =========================================================
# GROUP EXTRACTION
# =========================================================


def _get_group_list(value: str) -> list[str]:
    groups: set[str] = set()

    for regex_str in REGEX_LIST:
        pattern = re.compile(regex_str, re.IGNORECASE)
        for match in pattern.finditer(value):
            group = match.group()

            if group and not _is_space(group):
                groups.add(group.strip())

    # equivalent to Java: sorted by length ascending
    return sorted(groups, key=len)

# =========================================================
# HELPERS
# =========================================================


def _is_space(value: str) -> bool:
    return bool(re.fullmatch(r"\s\s*", value))


def _special_chars_only(value: str) -> bool:
    for ch in value:
        if ch not in SPECIAL_CHARS_REGEX:
            return False
    return True

# =========================================================
# Transform a time period into number.
# @param timePeriod The original time period (E.g.: 'i', '5' etc.)
# @param isDate Flag indicating if the input timePeriod is a date
# (E.g.: "01.10.1929", "1709, decembrie 24", etc.)
# @return The number that represents the time period (E.g.: 5, 9 etc.)
# =========================================================


def time_period_to_number(time_period: str, is_date: bool) -> int | None:
    # E.g.: "1/2 mil. 5 - sec. i al mil. 4 a.chr."
    if time_period is None or time_period.strip() == "":
        return None

    cleared = (
        clear_date(time_period)
        if is_date
        else time_period
    )

    cleared = clear_christum_notation(cleared)

    try:
        return int(cleared)
    except Exception:
        try:
            return roman_to_int(cleared).integer
        except Exception:
            return None

# =========================================================
# INTERVAL START
# =========================================================


def get_start_time(interval_values: list[str], era_start: str, is_date: bool) -> int | None:
    first = time_period_to_number(interval_values[0], is_date)
    second = time_period_to_number(interval_values[1], is_date)

    # E.g.: "prima jum. a sec. xxxxiv - xxxv a.ch."
    # "xxxxiv" is an invalid roman numeral
    if first is None or second is None:
        return None

    is_ad = era_start is not None and era_start == CHRISTUM_AD_PLACEHOLDER

    if is_ad and first > second:
        return second

    # E.g. "sec. ii a.chr. - sec. i p.chr."
    return first

# =========================================================
# INTERVAL END
# =========================================================


def get_end_time(interval_values: list[str], era_start: str, is_date: bool) -> int | None:
    first = time_period_to_number(interval_values[0], is_date)
    second = time_period_to_number(interval_values[1], is_date)

    # E.g.: "prima jum. a sec. xxxxiv - xxxv a.ch."
    # "xxxxiv" is an invalid roman numeral
    if first is None or second is None:
        return None

    is_ad = era_start is not None and era_start == CHRISTUM_AD_PLACEHOLDER

    if is_ad and first > second:
        return first

    # E.g. "sec. ii a.chr. - sec. i p.chr."
    return second
