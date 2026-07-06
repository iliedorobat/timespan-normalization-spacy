from __future__ import annotations

from dataclasses import dataclass

from temporal_normalization.commons_temporal import (
    century_to_millennium,
    clear_christum_notation,
    EMPTY_VALUE_PLACEHOLDER,
    get_era_name,
)
from temporal_normalization.commons_temporal.date_utils import get_month_name
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules.date import DATE_SEPARATOR


@dataclass
class LongDateModel(TimePeriodModel):
    """
    Used for those time intervals that are stored as a "long" date
    format (having a century, a year, a month and a day)
    E.g.: "s:17;a:1622;l:12;z:30"
    """

    # Java suffix constants
    SUFFIX_CENTURY: str = "s:"
    SUFFIX_YEAR: str = "a:"
    SUFFIX_MONTH: str = "l:"
    SUFFIX_DAY: str = "z:"

    def __init__(self, original: str, value: str, historical_only: bool):
        super().__init__()

        prepared_value = clear_christum_notation(value)
        values = prepared_value.split(DATE_SEPARATOR)

        self._set_era(value)

        for item in values:
            comparator = item.lower()

            if self.SUFFIX_CENTURY in comparator:
                self._set_century(item)
                self._set_millennium(item)

            elif self.SUFFIX_YEAR in comparator:
                self._set_year(item)

            elif self.SUFFIX_MONTH in comparator:
                self._set_month(item)

            elif self.SUFFIX_DAY in comparator:
                self._set_day(item)

    def _set_era(self, value: str):
        era = get_era_name(value)
        self.era_start = era
        self.era_end = era

    def _set_millennium(self, century_value: str):
        century_str = (
            century_value
            .replace(self.SUFFIX_CENTURY, EMPTY_VALUE_PLACEHOLDER)
            .strip()
        )

        try:
            century = int(century_str)
            millennium = century_to_millennium(century).millennium
            self.millennium_start = millennium
            self.millennium_end = millennium
        except ValueError as e:
            print(e)

    def _set_century(self, value: str):
        century_str = (
            value
            .replace(self.SUFFIX_CENTURY, EMPTY_VALUE_PLACEHOLDER)
            .strip()
        )

        try:
            century = int(century_str)
            self.century_start = century
            self.century_end = century
        except ValueError as e:
            print(e)

    def _set_year(self, value: str):
        year_str = (
            value
            .replace(self.SUFFIX_YEAR, EMPTY_VALUE_PLACEHOLDER)
            .strip()
        )

        try:
            year = int(year_str)
            self.year_start = year
            self.year_end = year
        except ValueError as e:
            print(e)

    def _set_month(self, value: str):
        month_str = (
            value
            .replace(self.SUFFIX_MONTH, EMPTY_VALUE_PLACEHOLDER)
            .strip()
        )

        month = get_month_name(month_str)
        self.month_start = month
        self.month_end = month

    def _set_day(self, value: str):
        day_str = (
            value
            .replace(self.SUFFIX_DAY, EMPTY_VALUE_PLACEHOLDER)
            .strip()
        )

        try:
            day = int(day_str)
            self.day_start = day
            self.day_end = day
        except ValueError as e:
            print(e)
