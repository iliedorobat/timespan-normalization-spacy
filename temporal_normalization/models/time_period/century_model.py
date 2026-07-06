from __future__ import annotations

from dataclasses import dataclass

import regex

from temporal_normalization.commons_temporal import (
    END_PLACEHOLDER,
    get_end_time,
    get_start_time,
    START_PLACEHOLDER,
    time_period_to_number,
)
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import (
    REGEX_INTERVAL_CONJUNCTION,
)


@dataclass(init=False)
class CenturyModel(TimePeriodModel):
    """
    Model pentru intervale de tip secol.
    """

    def __init__(self, original: str, value: str, regex_str: str, historical_only: bool):
        super().__init__()

        self.original = original
        self.value = value
        # TODO: rename it to regex_str
        self.regex = regex_str
        self.historical_only = historical_only

        self.set_century_model(original, value, regex_str, historical_only)

    def set_century_model(
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

            self.set_century_date(original, end_value, END_PLACEHOLDER, historical_only)
            self.set_century_date(original, start_value, START_PLACEHOLDER, historical_only)

        else:
            self.set_era(original, prepared_value, prepared_value, False)

            century_value = time_period_to_number(prepared_value, False)

            self.set_century_date(original, century_value, END_PLACEHOLDER, historical_only)
            self.set_century_date(original, century_value, START_PLACEHOLDER, historical_only)

    def set_century_date(
            self,
            original: str,
            century: int | None,
            position: str,
            historical_only: bool,
    ) -> None:
        if century is not None:
            self.set_century(original, century, position, historical_only)
