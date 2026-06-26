import re
from dataclasses import dataclass
from typing import Optional

from temporal_normalization.rules import AGE_BC, AGE_AD
from temporal_normalization.rules.imprecise import APPROX_NOTATION

# =========================================================
# CONSTANTS (ERA NORMALIZATION)
# =========================================================

CHRISTUM_AD_PLACEHOLDER = "__AD__"
CHRISTUM_BC_PLACEHOLDER = "__BC__"

CHRISTUM_AD_LABEL = "AD"
CHRISTUM_BC_LABEL = "BC"


START_PLACEHOLDER = "START"
END_PLACEHOLDER = "END"


DMY_PLACEHOLDER = "DMY"
YMD_PLACEHOLDER = "YMD"
MY_PLACEHOLDER = "MY"


# =========================================================
# ROMAN MAPS
# =========================================================

_ARABIC_TO_ROMAN = {
    1000: "m",
    900: "cm",
    500: "d",
    400: "cd",
    100: "c",
    90: "xc",
    50: "l",
    40: "xl",
    10: "x",
    9: "ix",
    5: "v",
    4: "iv",
    1: "i",
}

_ROMAN_TO_ARABIC = {
    "i": 1,
    "v": 5,
    "x": 10,
    "l": 50,
    "c": 100,
    "d": 500,
    "m": 1000,
}

# TODO: check (I added flags=re.IGNORECASE)
_ROMAN_PATTERN = re.compile(
    r"^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$", flags=re.IGNORECASE
)


# =========================================================
# DATACLASSES (PIPELINE OUTPUTS)
# =========================================================

@dataclass(frozen=True)
class EraInfo:
    raw: str
    normalized: str
    label: str


@dataclass(frozen=True)
class RomanParseResult:
    value: str
    is_valid: bool
    integer: Optional[int]


@dataclass(frozen=True)
class OrdinalResult:
    value: int
    ordinal: str


@dataclass(frozen=True)
class MillenniumResult:
    input_value: int
    millennium: int


# =========================================================
# ERA PIPELINE
# =========================================================

def normalize_christum_notation(value: str) -> str:
    """
    Normalize Christum notation as follows:
    - AGE_BC → "__BC__"
    - AGE_AD → "__AD__"
    """
    value = re.sub(AGE_BC, CHRISTUM_BC_PLACEHOLDER, value)
    value = re.sub(AGE_AD, CHRISTUM_AD_PLACEHOLDER, value)
    return value


def get_era_info(value: str) -> EraInfo:
    normalized = normalize_christum_notation(value)

    label = (
        CHRISTUM_BC_LABEL
        if CHRISTUM_BC_PLACEHOLDER in normalized
        else CHRISTUM_AD_LABEL
    )

    return EraInfo(
        raw=value,
        normalized=normalized,
        label=label,
    )


def get_era_name(value: str) -> str:
    return (
        CHRISTUM_BC_PLACEHOLDER
        if CHRISTUM_BC_PLACEHOLDER in value
        else CHRISTUM_AD_PLACEHOLDER
    )


def clear_christum_notation(value: str) -> str:
    return (
        value
        .replace(CHRISTUM_BC_PLACEHOLDER, "")
        .replace(CHRISTUM_AD_PLACEHOLDER, "")
        .strip()
    )


# =========================================================
# DATE CLEANING PIPELINE STEP
# =========================================================

def clear_date(value: str) -> str:
    """
    Remove inaccurate notations and normalize punctuation noise.
    """
    value = re.sub(APPROX_NOTATION, "", value)
    value = re.sub(r"[.\(\)\[\]\s]*", "", value)
    return value.strip()


# =========================================================
# ROMAN NUMERALS PIPELINE
# =========================================================

def int_to_roman(num: int) -> str:
    result = []

    for k in sorted(_ARABIC_TO_ROMAN.keys(), reverse=True):
        result.append(_ARABIC_TO_ROMAN[k] * (num // k))
        num %= k

    return "".join(result)


def roman_to_int(value: str) -> RomanParseResult:
    if not value or not value.strip():
        return RomanParseResult(value=value, is_valid=False, integer=None)

    roman = value.lower()

    # E.g.: "XIC" (89) is incorrect. The correct number is "LXXXIX" (89).
    if not _ROMAN_PATTERN.match(roman):
        return RomanParseResult(value=value, is_valid=False, integer=None)

    total = 0

    for i in range(len(roman) - 1):
        curr = _ROMAN_TO_ARABIC[roman[i]]
        nxt = _ROMAN_TO_ARABIC[roman[i + 1]]
        total += -curr if curr < nxt else curr

    total += _ROMAN_TO_ARABIC[roman[-1]]

    return RomanParseResult(value=value, is_valid=True, integer=total)


# =========================================================
# ORDINAL PIPELINE STEP
# =========================================================

def get_ordinal(value: int) -> OrdinalResult:
    suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6

    if 11 <= value % 100 <= 13:
        return OrdinalResult(value, f"{value}th")

    return OrdinalResult(value, f"{value}{suffixes[value % 10]}")


# =========================================================
# TEMPORAL CONVERSIONS
# =========================================================

def century_to_millennium(century: int) -> MillenniumResult:
    return MillenniumResult(
        input_value=century,
        millennium=-(-century // 10),
    )


def year_to_millennium(year: int) -> MillenniumResult:
    return MillenniumResult(
        input_value=year,
        millennium=-(-year // 1000),
    )