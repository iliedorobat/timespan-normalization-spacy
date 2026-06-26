from __future__ import annotations

from dataclasses import dataclass

from temporal_normalization.commons import (
    clear_christum_notation,
    END_PLACEHOLDER,
    MY_PLACEHOLDER,
    START_PLACEHOLDER,
)
from temporal_normalization.commons_temporal.date_utils import Date
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import REGEX_INTERVAL_DELIMITER, REGEX_DATE_SEPARATOR


@dataclass
class ShortDateModel(TimePeriodModel):
    """
    Used for date presented as month-year format
    E.g.:
         * MY: "octombrie 1639"; "ianuarie 632";
               "septembrie - octombrie 1919"; "09 1875"
    """

    def __init__(self, original: str, value: str, order: str, historical_only: bool):
        super().__init__()
        self._set_date_model(original, value, order, historical_only)

    def _set_date_model(self, original: str, value: str, order: str, historical_only: bool):
        interval_values = value.split(REGEX_INTERVAL_DELIMITER)

        if len(interval_values) == 2:
            self.set_era(original, interval_values[0], interval_values[1], True)

            end_month = self._get_month(interval_values[0])
            end_year = self._get_year(interval_values[0], interval_values[1], order, END_PLACEHOLDER)
            self._set_date(original, end_year, end_month, order, END_PLACEHOLDER, historical_only)

            start_month = self._get_month(interval_values[1])
            start_year = self._get_year(interval_values[0], interval_values[1], order, START_PLACEHOLDER)
            self._set_date(original, start_year, start_month, order, START_PLACEHOLDER, historical_only)

        else:
            self.set_era(original, value, value, True)

            end_month = self._get_month(value)
            end_year = self._get_year(value, value, order, END_PLACEHOLDER)
            self._set_date(original, end_year, end_month, order, END_PLACEHOLDER, historical_only)

            start_month = self._get_month(value)
            start_year = self._get_year(value, value, order, START_PLACEHOLDER)
            self._set_date(original, start_year, start_month, order, START_PLACEHOLDER, historical_only)

    def _set_date(
            self,
            original: str,
            year: str,
            month: str,
            order: str,
            position: str,
            historical_only: bool,
    ):
        if order == MY_PLACEHOLDER:
            self.set_millennium_from_year(original, year, position, historical_only)
            self.set_century_from_year(original, year, position, historical_only)
            self.set_year(original, year, position, historical_only)
            self.set_month(original, month, position, historical_only)

    def _get_year(self, start_date: str, end_date: str, order: str, position: str):
        start_values = self._split_date(start_date)
        end_values = self._split_date(end_date)

        if order == MY_PLACEHOLDER:

            if position == START_PLACEHOLDER:

                if len(start_values) > 1:
                    return start_values[1]

                # Avoids the "Invalid month number" warning thrown by the "getMonth" method
                if len(start_values[0]) > 2:
                    # E.g.: "629-ianuarie 632"
                    return start_values[0]

                return (
                    start_values[0]
                    if self._get_month(start_values[0]) == "Unknown"
                    # E.g.: "septembrie - octombrie 1919"
                    else end_values[1]
                )

            elif position == END_PLACEHOLDER:

                # E.g.: "noiembrie 1784 - aprilie 1785"
                if len(end_values) > 1:
                    return end_values[1]

                # E.g.: "noiembrie 1784 - 1785"
                return end_values[0]

        return None

    def _get_month(self, date: str):
        prepared_value = Date.prepare_date(date)
        values = prepared_value.split(REGEX_DATE_SEPARATOR)

        return Date.get_month_name(values[0].strip())

    def _split_date(self, date: str):
        prepared_value = clear_christum_notation(date)
        prepared_value = Date.prepare_date(prepared_value)

        return prepared_value.split(REGEX_DATE_SEPARATOR)
