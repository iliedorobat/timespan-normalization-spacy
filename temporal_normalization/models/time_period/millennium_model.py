from __future__ import annotations

from dataclasses import dataclass

import regex

from temporal_normalization.commons import (
    END_PLACEHOLDER,
    get_end_time,
    get_start_time,
    START_PLACEHOLDER,
    time_period_to_number,
)
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import (
    REGEX_INTERVAL_DELIMITER, REGEX_INTERVAL_CONJUNCTION,
)


@dataclass(init=False)
class MillenniumModel(TimePeriodModel):
    """
    Model pentru intervale de tip mileniu.
    """

    def __init__(self, original: str, value: str, regex_str: str, historical_only: bool):
        super().__init__()

        self.original = original
        self.value = value
        # TODO: rename it to regex_str
        self.regex = regex_str
        self.historical_only = historical_only

        self.set_millennium_model(original, value, regex_str, historical_only)

    def set_millennium_model(
            self,
            original: str,
            value: str,
            regex_str: str,
            historical_only: bool,
    ) -> None:
        prepared_value = self.prepare_value(value, regex_str)
        interval_values = regex.split(REGEX_INTERVAL_CONJUNCTION, prepared_value, flags=regex.IGNORECASE)

        if len(interval_values) == 2:
            self.set_era(original, interval_values[0], interval_values[1], False)

            end_value = get_end_time(
                interval_values,
                self.era_start,
                False,
            )
            start_value = get_start_time(
                interval_values,
                self.era_start,
                False,
            )

            self.set_millennium_date(original, end_value, END_PLACEHOLDER, historical_only)
            self.set_millennium_date(original, start_value, START_PLACEHOLDER, historical_only)

        else:
            self.set_era(original, value, value, False)

            millennium_value = time_period_to_number(prepared_value, False)

            self.set_millennium_date(original, millennium_value, END_PLACEHOLDER, historical_only)
            self.set_millennium_date(original, millennium_value, START_PLACEHOLDER, historical_only)

    def set_millennium_date(
            self,
            original: str,
            millennium: int | None,
            position: str,
            historical_only: bool,
    ) -> None:
        if millennium is not None:
            self.set_millennium(original, millennium, position, historical_only)
