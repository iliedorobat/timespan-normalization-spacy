from __future__ import annotations

import re
from dataclasses import dataclass

from .time_period_model import TimePeriodModel
from temporal_normalization.commons import clear_christum_notation, END_PLACEHOLDER, START_PLACEHOLDER, sanitize_time_period
from temporal_normalization.rules import CASE_INSENSITIVE, REGEX_INTERVAL_PREFIX, REGEX_INTERVAL_CONJUNCTION, REGEX_INTERVAL_DELIMITER
from temporal_normalization.rules.year import YEAR_INTERVAL_PREFIXED, YEAR_OR_SEPARATOR


@dataclass
class YearModel(TimePeriodModel):
    """
    Equivalent of Java YearModel extending TimePeriodModel.
    """

    # Used to separate the minus sign from the dash separator "-2 - -14 p.chr"; "-2 p.chr - -14 p.chr"
    REGEX_AGE_SEPARATOR: str = r"(?<=[\wăâîşșţțĂÂÎŞȘŢȚ\W&&[^ -]])[ ]*-[ ]*"

    def __init__(self, original: str = None, value: str = None, regex: str = None, historical_only: bool = False):
        super().__init__()

        if original is not None and value is not None and regex is not None:
            self.set_year_model(original, value, regex, historical_only)

    # =========================================================
    # setYearModel()
    # =========================================================

    def set_year_model(self, original: str, value: str, regex: str, historical_only: bool):
        prepared_value = self.prepare_value(value, regex)
        interval_values = re.split(REGEX_INTERVAL_DELIMITER, prepared_value, flags=re.IGNORECASE)

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
    # prepareValue()
    # =========================================================

    def prepare_value(self, value: str, regex: str) -> str:
        if regex == YEAR_INTERVAL_PREFIXED:
            prepared_value = re.sub(REGEX_INTERVAL_PREFIX, "", value, flags=re.IGNORECASE)
            prepared_value = re.sub(REGEX_INTERVAL_CONJUNCTION, " - ", prepared_value, flags=re.IGNORECASE)
            return sanitize_time_period(prepared_value.strip())

        prepared_value = re.sub(YEAR_OR_SEPARATOR, " - ", value, flags=re.IGNORECASE)
        return sanitize_time_period(prepared_value.strip())

    # =========================================================
    # setDate()
    # =========================================================

    def _set_date(self, original: str, year: str, position: str, historical_only: bool):
        self.set_millennium_from_year(original, year, position, historical_only)
        self.set_century_from_year(original, year, position, historical_only)
        self.set_year(original, year, position, historical_only)
