from __future__ import annotations

from dataclasses import dataclass

import regex

from temporal_normalization.commons import (
    clear_christum_notation,
    DMY_PLACEHOLDER,
    END_PLACEHOLDER,
    START_PLACEHOLDER,
    YMD_PLACEHOLDER,
)
from temporal_normalization.commons_temporal.date_utils import Date
from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import REGEX_INTERVAL_DELIMITER


@dataclass
class DateModel(TimePeriodModel):
    """
    Used for date presented as day-month-year or year-month-day format.
    E.g.:
         * DMY: "14 ianuarie 1497", "21/01/1916", "01.11.1668", "1.09.1607", "17/29 octombrie 1893";
                "dupa 29 aprilie 1616"; "dupa 10 mai 1903";
         * YMD: "1974-05-05", "1891 decembrie 07", "1738, MAI, 4"
    """

    def __init__(self, original: str, value: str, order: str, historical_only: bool):
        super().__init__()
        self._set_date_model(original, value, order, historical_only)

    def _set_date_model(self, original: str, value: str, order: str, historical_only: bool):
        interval_values = regex.split(REGEX_INTERVAL_DELIMITER, value, flags=regex.IGNORECASE)

        if len(interval_values) == 2:
            self.set_era(
                original,
                self._get_year(interval_values[0], interval_values[1], order),
                self._get_year(interval_values[1], interval_values[0], order),
                True,
            )

            self._set_date(
                original,
                interval_values[0],
                interval_values[1],
                order,
                END_PLACEHOLDER,
                historical_only,
            )

            self._set_date(
                original,
                interval_values[0],
                interval_values[1],
                order,
                START_PLACEHOLDER,
                historical_only,
            )

        else:
            self.set_era(
                original,
                self._get_year(value, value, order),
                self._get_year(value, value, order),
                True,
            )

            self._set_date(
                original,
                value,
                value,
                order,
                END_PLACEHOLDER,
                historical_only,
            )

            self._set_date(
                original,
                value,
                value,
                order,
                START_PLACEHOLDER,
                historical_only,
            )

    def _set_date(
            self,
            original: str,
            start_date: str,
            end_date: str,
            order: str,
            position: str,
            historical_only: bool,
    ):
        start = clear_christum_notation(start_date)
        end = clear_christum_notation(end_date)

        main_date = start if position == START_PLACEHOLDER else end
        second_date = end if position == START_PLACEHOLDER else start

        self._set_date_time(original, main_date, second_date, order, position, historical_only)

    def _set_date_time(
            self,
            original: str,
            first_date: str,
            second_date: str,
            order: str,
            position: str,
            historical_only: bool,
    ):
        year = self._get_year(first_date, second_date, order)
        month = self._get_month(first_date, second_date, order)
        day = self._get_day(first_date, second_date, order)

        self.set_millennium_from_year(original, year, position, historical_only)
        self.set_century_from_year(original, year, position, historical_only)
        self.set_year(original, year, position, historical_only)
        self.set_month(original, month, position, historical_only)
        self.set_day(original, day, position, historical_only)

    @staticmethod
    def _get_year(main_date: str, second_date: str, order: str):
        values = Date.get_atomic_values(main_date)

        try:
            # values.length == 4 if the month name is abbreviated (E.g.: "aug.")
            if order == DMY_PLACEHOLDER:
                return values[3] if len(values) == 4 else values[2]

            if order == YMD_PLACEHOLDER:
                return values[0]

        except IndexError:
            return DateModel._get_year(second_date, main_date, order)

        except Exception as e:
            print(e)
            return None

        return None

    @staticmethod
    def _get_month(main_date: str, second_date: str, order: str):
        values = Date.get_atomic_values(main_date)

        if order in (DMY_PLACEHOLDER, YMD_PLACEHOLDER):
            try:
                return Date.get_month_name(values[1].strip())

            except IndexError:
                # E.g.: 19-26 noiembrie 2010
                second_values = Date.get_atomic_values(second_date)
                return Date.get_month_name(second_values[1].strip())

            except Exception as e:
                print(e)
                return None

        return None

    @staticmethod
    def _get_day(main_date: str, second_date: str, order: str):
        values = Date.get_atomic_values(main_date)

        if order == DMY_PLACEHOLDER:
            return values[0]

        if order == YMD_PLACEHOLDER:
            return values[3] if len(values) == 4 else values[2]

        return None
