from __future__ import annotations

from dataclasses import dataclass

import regex

from temporal_normalization.commons import clear_christum_notation, END_PLACEHOLDER, START_PLACEHOLDER
from temporal_normalization.rules import REGEX_INTERVAL_DELIMITER
from .time_period_model import TimePeriodModel


@dataclass
class YearModel(TimePeriodModel):
    """
    Equivalent of Java YearModel extending TimePeriodModel.
    """

    # Used to separate the minus sign from the dash separator "-2 - -14 p.chr"; "-2 p.chr - -14 p.chr"
    REGEX_AGE_SEPARATOR: str = r"(?<=[\wăâîşșţțĂÂÎŞȘŢȚ\W&&[^ -]])[ ]*-[ ]*"

    def __init__(self, original: str = None, value: str = None, regex_str: str = None, historical_only: bool = False):
        super().__init__()

        if original is not None and value is not None and regex_str is not None:
            self.set_year_model(original, value, regex_str, historical_only)

    # =========================================================
    # setYearModel()
    # =========================================================

    def set_year_model(self, original: str, value: str, regex_str: str, historical_only: bool):
        prepared_value = self.prepare_value(value, regex_str)
        interval_values = regex.split(REGEX_INTERVAL_DELIMITER, prepared_value, flags=regex.IGNORECASE)

        if len(interval_values) == 2:
            self.set_era(original, interval_values[0], interval_values[1], True)

            end_year = clear_christum_notation(interval_values[1])
            start_year = clear_christum_notation(interval_values[0])

            self._set_date(original, end_year, END_PLACEHOLDER, historical_only)
            self._set_date(original, start_year, START_PLACEHOLDER, historical_only)

        else:
            self.set_era(original, value, value, True)

            year_value = clear_christum_notation(prepared_value)

            self._set_date(original, year_value, END_PLACEHOLDER, historical_only)
            self._set_date(original, year_value, START_PLACEHOLDER, historical_only)

    # =========================================================
    # setDate()
    # =========================================================

    def _set_date(self, original: str, year: str, position: str, historical_only: bool):
        self.set_millennium_from_year(original, year, position, historical_only)
        self.set_century_from_year(original, year, position, historical_only)
        self.set_year(original, year, position, historical_only)
