from __future__ import annotations

from dataclasses import dataclass

import regex

from temporal_normalization.commons_temporal import (
    clear_christum_notation,
    EMPTY_VALUE_PLACEHOLDER,
    END_PLACEHOLDER,
    START_PLACEHOLDER,
)
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import REGEX_INTERVAL_DELIMITER


@dataclass(init=False)
class InaccurateYearModel(TimePeriodModel):
    """
    E.g.: "aprox. 1900"
    """

    # TODO: find a way to store the detail for inaccurate time periods
    # (after, before, approx.)

    REGEX_NON_DIGIT = r"[^\d]"

    def __init__(self, original: str, value: str, historical_only: bool):
        super().__init__()

        self.original = original
        self.value = value
        self.historical_only = historical_only

        self.set_date_model(original, value, historical_only)

    def set_date_model(self, original: str, value: str, historical_only: bool) -> None:
        interval_values = regex.split(REGEX_INTERVAL_DELIMITER, value, flags=regex.IGNORECASE)

        if len(interval_values) == 2:
            self.set_era(original, interval_values[0], interval_values[1], True)

            start_value = clear_christum_notation(interval_values[0])
            end_value = clear_christum_notation(interval_values[1])

            self.set_date(original, end_value, END_PLACEHOLDER, historical_only)
            self.set_date(original, start_value, START_PLACEHOLDER, historical_only)

        else:
            self.set_era(original, value, value, True)

            prepared_value = clear_christum_notation(value)

            self.set_date(original, prepared_value, END_PLACEHOLDER, historical_only)
            self.set_date(original, prepared_value, START_PLACEHOLDER, historical_only)

    def set_date(self, original: str, value: str, position: str, historical_only: bool) -> None:
        year = regex.sub(self.REGEX_NON_DIGIT, EMPTY_VALUE_PLACEHOLDER, value)

        self.set_millennium_from_year(original, year, position, historical_only)
        self.set_century_from_year(original, year, position, historical_only)
        self.set_year(original, year, position, historical_only)
