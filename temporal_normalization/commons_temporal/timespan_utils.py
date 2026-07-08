import re
from typing import List

import regex

from temporal_normalization.commons_temporal import (
    DMY_PLACEHOLDER,
    EMPTY_VALUE_PLACEHOLDER,
    normalize_christum_notation,
    MY_PLACEHOLDER,
    STRING_LIST_SEPARATOR,
    TemporalType,
    YMD_PLACEHOLDER,
)
from temporal_normalization.commons_temporal.time_sanitize_utils import clear_junks, sanitize_value
from temporal_normalization.models import YearModel, TimespanModel, AgeModel
from temporal_normalization.models.date import LongDateModel, ShortDateModel, DateModel
from temporal_normalization.models.imprecise import InaccurateYearModel, DatelessModel
from temporal_normalization.models.time_period import CenturyModel, MillenniumModel
from temporal_normalization.rules import (
    AGE_OPTIONS,
    AGE_REGEXES,
    CENTURY_INTERVAL_PREFIXED,
    CENTURY_INTERVAL_BASE,
    CENTURY_OPTIONS,
    CENTURY_REGEXES,
    MILLENNIUM_INTERVAL_PREFIXED,
    MILLENNIUM_INTERVAL_BASE,
    MILLENNIUM_OPTIONS,
    MILLENNIUM_REGEXES,
    OTHER_CENTURY_ROMAN_INTERVAL,
    OTHER_CENTURY_ROMAN_OPTIONS,
    UNKNOWN_REGEXES,
)
from temporal_normalization.rules.date import (
    DATE_DMY_INTERVAL,
    DATE_DMY_INTERVAL_PARTIAL,
    DATE_YMD_INTERVAL,
    DATE_DMY_OPTIONS,
    DATE_YMD_OPTIONS,
    DATE_MY_OPTIONS,
    DATE_MY_INTERVAL,
    LONG_DATE_OPTIONS,
    LONG_DATE_REGEXES,
    DATE_MY_REGEXES,
    DATE_YMD_REGEXES,
    DATE_DMY_REGEXES,
)
from temporal_normalization.rules.imprecise import (
    AFTER,
    AFTER_INTERVAL,
    BEFORE,
    BEFORE_INTERVAL,
    APPROX_AGES_INTERVAL,
    APPROX_AGES_OPTIONS,
    DATELESS_REGEXES,
    INACCURATE_YEAR_REGEXES,
)
from temporal_normalization.rules.year import (
    YEAR_INTERVAL_PREFIXED,
    YEAR_INTERVAL_BASE,
    YEAR_3_4_DIGITS_SPECIAL_INTERVAL,
    YEAR_OPTIONS,
    UNKNOWN_YEARS,
    YEAR_REGEXES,
)


def prepare_timespan_models(original: str, historical_only: bool, sanitize: bool) -> List["TimespanModel"]:
    """
    In the matching process the first matched value need to be the interval type,
    followed by the ordinal values, respecting the following order:
    <ol>
        <li>Map every unknown value in order to clear the list by junk elements</li>
        <li>Map every date-like value</li>
        <li>Map every century and millennium age-like value</li>
        <li>Map every epoch-like value</li>
        <li>Map unprecise years</li>
        <li>Map years</li>
        <li>Map unknown years</li>
    </ol>
    @param original The original value taken from "lido:displayDate" record
    @param historicalOnly Flag which specifies whether the Framework will only handle
                           historical dates (future dates will be ignored)
    @param sanitize Flag specifying if the custom method sanitizeValue
                    will be used to sanitize values. Use "true" only if you use this
                    framework on LIDO datasets.
    """
    residual_value = sanitize_value(original)
    timespan_models: List["TimespanModel"] = []

    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, UNKNOWN_REGEXES, TemporalType.UNKNOWN)

    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_DMY_INTERVAL, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_DMY_INTERVAL_PARTIAL, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_YMD_INTERVAL, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_MY_INTERVAL, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_DMY_OPTIONS, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_YMD_OPTIONS, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATE_MY_OPTIONS, TemporalType.DATE)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, LONG_DATE_OPTIONS, TemporalType.DATE)

    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, CENTURY_INTERVAL_PREFIXED, TemporalType.CENTURY)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, CENTURY_INTERVAL_BASE, TemporalType.CENTURY)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, CENTURY_OPTIONS, TemporalType.CENTURY)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, MILLENNIUM_INTERVAL_PREFIXED, TemporalType.MILLENNIUM)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, MILLENNIUM_INTERVAL_BASE, TemporalType.MILLENNIUM)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, MILLENNIUM_OPTIONS, TemporalType.MILLENNIUM)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, OTHER_CENTURY_ROMAN_INTERVAL, TemporalType.CENTURY)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, OTHER_CENTURY_ROMAN_OPTIONS, TemporalType.CENTURY)

    for i in range(len(AGE_OPTIONS)):
        residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, AGE_OPTIONS[i], TemporalType.EPOCH)

    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, AFTER_INTERVAL, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, BEFORE_INTERVAL, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, APPROX_AGES_INTERVAL, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, YEAR_INTERVAL_PREFIXED, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, YEAR_INTERVAL_BASE, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, YEAR_3_4_DIGITS_SPECIAL_INTERVAL, TemporalType.YEAR)

    # if sanitize:
    #     residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATELESS_MODEL_X, TemporalType.YEAR)
    #     residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATELESS_UNDATED, TemporalType.YEAR)
    #     residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, DATELESS, TemporalType.UNKNOWN)

    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, AFTER, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, BEFORE, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, APPROX_AGES_OPTIONS, TemporalType.YEAR)
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, YEAR_OPTIONS, TemporalType.YEAR)

    # This call must be made after all processing performed on calendar years!!!
    residual_value = update_matched_values(residual_value, timespan_models, historical_only, sanitize, UNKNOWN_YEARS, TemporalType.UNKNOWN)

    return timespan_models


# TODO: rename regex_str to pattern
def update_matched_values(
        original,
        timespan_models,
        historical_only,
        sanitize,
        regex_str,
        matched_type
):
    residual_value = (
        clear_junks(original, regex_str)
        if sanitize
        else original
    )

    pattern = regex.compile(regex_str, flags=re.IGNORECASE)

    for match in pattern.finditer(residual_value):
        matched_value = match.group()
        if matched_value is None:
            continue

        matched_value = matched_value.strip()

        time_period = prepare_time_period_model(
            original,
            normalize_christum_notation(matched_value),
            regex_str,
            historical_only
        )

        matched_items = str(time_period)

        if matched_items and matched_items != matched_value:
            matched_list = matched_items.split(STRING_LIST_SEPARATOR)

            timespan_models.append(
                TimespanModel(
                    time_period,
                    matched_list,
                    matched_value,
                    matched_type,
                    residual_value
                )
            )

        elif matched_items == matched_value:
            print(f'The following group has not been processed: "{matched_value}"')

    residual_value = regex.sub(regex_str, EMPTY_VALUE_PLACEHOLDER, residual_value, flags=regex.IGNORECASE)

    return residual_value


def prepare_time_period_model(original: str, value: str, regex_str: str, historical_only: bool):
    """
    Ensure the right format for date-like, year-like, centuries and millenniums values
    @param original The original value
    @param value The value subjected to the replacement process (part of the original value)
    @param regex_str The regular expression that defines a search pattern
    @param historical_only Flag which specifies whether the Framework will only handle historical
                           dates (future dates will be ignored)
    @return The formatted value
    """
    prepared = prepare_ages(original, value, regex_str, historical_only)

    if prepared is None:
        prepared = prepare_date_time(original, value, regex_str, historical_only)

    if prepared is None:
        prepared = prepare_period(original, value, regex_str, historical_only)

    return prepared


def prepare_ages(original: str, value: str, regex_str: str, historical_only: bool):
    """
    Ensure the right format for year-like value
    """
    if regex_str in INACCURATE_YEAR_REGEXES:
        return InaccurateYearModel(original, value, historical_only)
    elif regex_str in DATELESS_REGEXES:
        return DatelessModel(original, value, regex_str, historical_only)
    elif regex_str in YEAR_REGEXES:
        return YearModel(original, value, regex_str, historical_only)
    return None


def prepare_date_time(original: str, value: str, regex_str: str, historical_only: bool):
    """
    Ensure the right format for date-like value
    """
    if regex_str in DATE_DMY_REGEXES:
        return DateModel(original, value, DMY_PLACEHOLDER, historical_only)
    elif regex_str in DATE_YMD_REGEXES:
        return DateModel(original, value, YMD_PLACEHOLDER, historical_only)
    elif regex_str in DATE_MY_REGEXES:
        return ShortDateModel(original, value, MY_PLACEHOLDER, historical_only)
    elif regex_str in LONG_DATE_REGEXES:
        return LongDateModel(original, value, historical_only)
    else:
        return None


def prepare_period(original: str, value: str, regex_str: str, historical_only: bool):
    """
    Ensure the right format for centuries and millenniums
    """
    if regex_str in CENTURY_REGEXES:
        return CenturyModel(original, value, regex_str, historical_only)
    elif regex_str in MILLENNIUM_REGEXES:
        return MillenniumModel(original, value, regex_str, historical_only)
    elif regex_str in AGE_REGEXES:
        return AgeModel(original, value, regex_str, historical_only)
    else:
        return None
