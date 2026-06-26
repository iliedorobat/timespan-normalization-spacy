import re

from temporal_normalization.commons import EMPTY_VALUE_PLACEHOLDER
from temporal_normalization.rules.year import YEAR_3_4_DIGITS_SPECIAL_INTERVAL, YEAR_3_4_DIGITS_SPECIAL_PREFIX


def sanitize_value(value: str) -> str:
    """
    Sanitize some values that appear rarely and a regex operation
    would be time-consuming
    """
    sanitized = _sanitize_date_time(value)
    sanitized = _sanitize_ages(sanitized)
    sanitized = _sanitize_time_periods(sanitized)
    return sanitized


def clear_junks(value: str, regex: str) -> str:
    """
    Clean value by junks that could be interpreted by other regexes
    E.g.: "anul 13=1800/1801" will lead to "anul 13=" junk value.
    """
    if regex is not None and regex == YEAR_3_4_DIGITS_SPECIAL_INTERVAL:
        return re.sub(
            YEAR_3_4_DIGITS_SPECIAL_PREFIX,
            EMPTY_VALUE_PLACEHOLDER,
            value
        )
    return value


def _sanitize_date_time(value: str) -> str:
    """
    Sanitize date-like values that appear rarely and a regex operation
    would be time-consuming
    """
    match value:
        case "17 nov. 375-9 aug. 378 a.chr.":
            return "17 nov. 375 - 9 aug. 378 a.chr."
        case "[11-13 martie] 1528":
            return "11 martie 1528 - 13 martie 1528"
        case "6 octombrie1904":
            return "6 octombrie 1904"
        case "30 mai și 5 august 1796":
            return "30 mai 1796; 5 august 1796"
        case "1861septembrie 25":
            return "25 septembrie 1861"
        case "1908 martie 27-28":
            return "27 martie 1908 - 28 martie 1908"
        case "1834, 1 - 10 aprilie":
            return "1 aprilie 1834 - 10 aprilie 1834"
        case _:
            return value


def _sanitize_ages(value: str) -> str:
    """
    Sanitize year-like values that appear rarely and a regex operation
    would be time-consuming
    """
    if value == "1880 (proprietarul avea 90 de ani în 1970)":
        return "1880"
    return value


def _sanitize_time_periods(value: str) -> str:
    """
    Sanitize centuries and millenniums values that rarely appear
    and a regex operation would be time-consuming
    """
    match value:
        case "15(6)3":
            return "1563"
        case "1884 martie 28/aprilie 09":
            return "1884"
        case "octombrie 23, 1777":
            return "23 octombrie 1777"
        case "a doua jumatate a sec. i a.chr. (-43 - -29); a doua jum. a sec.xix (montură inel)":
            return "a doua jumatate a sec. i a.chr. (43 - 29 a.chr.); a doua jum. a sec.xix (montură inel)"
        case "instituit în decembrie 1915 - desființat în 1973":
            return "1915 - 1973"
        case "prima jumătate a secolului xviii (rest de datare 174...)":
            return "prima jumătate a secolului xviii"
        case "sec. xviii - xix 18(40)":
            return "sec. xviii - xix"
        case "281-222 (232?) p. chr.":
            return "281-222 p. chr."
        case "0803":
            return "unknown"
        case "13 (1805)":
            return "1805"
        case _:
            return value
