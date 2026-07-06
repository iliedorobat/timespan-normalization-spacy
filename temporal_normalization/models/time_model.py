from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from temporal_normalization.commons_temporal import (
    CHRISTUM_AD_PLACEHOLDER,
    CHRISTUM_BC_PLACEHOLDER,
    century_to_millennium,
    clear_date,
    END_PLACEHOLDER,
    get_era_name,
    LAST_UPDATE_YEAR,
    LAST_UPDATE_MILLENNIUM,
    LAST_UPDATE_CENTURY,
    PRINT_ERROR,
    START_PLACEHOLDER,
    time_period_to_number,
    year_to_millennium,
)
from temporal_normalization.errors.too_big_date import (
    TooBigCenturyError,
    TooBigMillenniumError,
    TooBigYearError,
)


@dataclass
class TimeModel:
    era_start: Optional[str] = None
    era_end: Optional[str] = None

    millennium_start: Optional[int] = None
    millennium_end: Optional[int] = None

    century_start: Optional[int] = None
    century_end: Optional[int] = None

    year_start: Optional[int] = None
    year_end: Optional[int] = None

    month_start: Optional[str] = None
    month_end: Optional[str] = None

    day_start: int = 0
    day_end: int = 0

    # =========================================================
    # ERA HANDLING
    # =========================================================

    def set_era(self, original: str, start_value: str, end_value: str, is_date: bool):
        has_start_era = self._has_christum_notation(start_value)
        has_end_era = self._has_christum_notation(end_value)

        if has_start_era and has_end_era:
            self.era_start = get_era_name(start_value)
            self.era_end = get_era_name(end_value)

        elif not has_start_era and not has_end_era:
            start = time_period_to_number(start_value, is_date)
            end = time_period_to_number(end_value, is_date)

            if start is None or end is None:
                self.era_start = CHRISTUM_AD_PLACEHOLDER
                self.era_end = CHRISTUM_AD_PLACEHOLDER

            elif start > end:
                self.era_start = CHRISTUM_BC_PLACEHOLDER
                self.era_end = CHRISTUM_BC_PLACEHOLDER

            else:
                self.era_start = CHRISTUM_AD_PLACEHOLDER
                self.era_end = CHRISTUM_AD_PLACEHOLDER

        # E.g.: "sec. i a.chr. - sec. i"
        elif has_start_era and not has_end_era:
            self.era_start = get_era_name(start_value)
            self.era_end = CHRISTUM_AD_PLACEHOLDER

        # E.g.: sec. 4 - sec. 2 p. chr.
        elif not has_start_era and has_end_era:
            self.era_end = get_era_name(end_value)

            start = time_period_to_number(start_value, is_date)
            end = time_period_to_number(end_value, is_date)

            if start is None or end is None:
                self.era_start = self.era_end

            elif start > end:
                self.era_start = CHRISTUM_BC_PLACEHOLDER

            else:
                self.era_start = self.era_end

    # =========================================================
    # MILLENNIUM
    # =========================================================

    def set_millennium_from_year(self, original: str, year_str: str, position: str, historical_only: bool):
        try:
            year = int(clear_date(year_str))

            if year > LAST_UPDATE_YEAR and self.era_start == CHRISTUM_AD_PLACEHOLDER:
                if historical_only:
                    raise TooBigMillenniumError(
                        f'setting millennium from "{original}"',
                        position,
                        year,
                    )

                if PRINT_ERROR:
                    TooBigMillenniumError.print_message(
                        f'setting millennium from "{original}"',
                        position,
                        year,
                    )

            millennium = year_to_millennium(year).millennium
            self.set_millennium(original, millennium, position, historical_only)

        except (ValueError, TooBigMillenniumError) as e:
            print(e)

    def set_millennium(self, original: str, millennium: int | None, position: str, historical_only: bool):
        try:
            if millennium is not None:

                if millennium > LAST_UPDATE_MILLENNIUM and self.era_start == CHRISTUM_AD_PLACEHOLDER:
                    if historical_only:
                        self.millennium_start = None
                        self.millennium_end = None

                        raise TooBigMillenniumError(
                            f'setting millennium from "{original}"',
                            position,
                            millennium,
                        )

                    if PRINT_ERROR:
                        TooBigMillenniumError.print_message(
                            f'setting millennium from "{original}"',
                            position,
                            millennium,
                        )

                if position == START_PLACEHOLDER:
                    self.millennium_start = millennium
                elif position == END_PLACEHOLDER:
                    self.millennium_end = millennium

        except TooBigMillenniumError as e:
            print(e)

    # =========================================================
    # CENTURY
    # =========================================================

    def set_century_from_year(self, original: str, year_str: str, position: str, historical_only: bool):
        try:
            year = int(clear_date(year_str))

            if year > LAST_UPDATE_YEAR and self.era_start == CHRISTUM_AD_PLACEHOLDER:
                if historical_only:
                    raise TooBigYearError(
                        f'setting century from "{original}"',
                        position,
                        year,
                    )

                if PRINT_ERROR:
                    TooBigYearError.print_message(
                        f'setting century from "{original}"',
                        position,
                        year,
                    )

            # E.g.: the year 100 is part of the first century
            # Math.floor(100 / 100) + 0 = 1st century
            # Math.floor(101 / 100) + 1 = 2nd century
            buffer = 0 if year % 100 == 0 else 1
            century = int(year / 100) + buffer

            self.set_century(original, century, position, historical_only)

        except (ValueError, TooBigYearError) as e:
            print(e)

    def set_century(self, original: str, century: int | None, position: str, historical_only: bool):
        try:
            if century is not None:

                if century > LAST_UPDATE_CENTURY and self.era_start == CHRISTUM_AD_PLACEHOLDER:
                    if historical_only:
                        self.century_start = None
                        self.century_end = None

                        raise TooBigCenturyError(
                            f'setting century from "{original}"',
                            position,
                            century,
                        )

                    if PRINT_ERROR:
                        TooBigCenturyError.print_message(
                            f'setting century from "{original}"',
                            position,
                            century,
                        )

                if position is not None:
                    millennium = century_to_millennium(century).millennium
                    self.set_millennium(original, millennium, position, historical_only)

                    if position == START_PLACEHOLDER:
                        self.century_start = century
                    elif position == END_PLACEHOLDER:
                        self.century_end = century

        except TooBigCenturyError as e:
            print(e)

    # =========================================================
    # YEAR
    # =========================================================

    def set_year(self, original: str, year_str: str, position: str, historical_only: bool):
        try:
            year = int(clear_date(year_str))

            if year > LAST_UPDATE_YEAR and self.era_start == CHRISTUM_AD_PLACEHOLDER:
                if historical_only:
                    raise TooBigYearError(
                        f'setting year from "{original}"',
                        position,
                        year,
                    )

                if PRINT_ERROR:
                    TooBigYearError.print_message(
                        f'setting year from "{original}"',
                        position,
                        year,
                    )

            if position == START_PLACEHOLDER:
                self.year_start = year
            elif position == END_PLACEHOLDER:
                self.year_end = year

        except (ValueError, TooBigYearError) as e:
            print(e)

    # =========================================================
    # MONTH
    # =========================================================

    def set_month(self, original: str, month: str, position: str, historical_only: bool):
        if position == START_PLACEHOLDER:
            self.month_start = month
        elif position == END_PLACEHOLDER:
            self.month_end = month

    # =========================================================
    # DAY
    # =========================================================

    def set_day(self, original: str, day_str: str, position: str, historical_only: bool):
        try:
            day = int(day_str)

            if position == START_PLACEHOLDER:
                self.day_start = day
            elif position == END_PLACEHOLDER:
                self.day_end = day

        except ValueError as e:
            print(e)

    # =========================================================
    # HELPERS
    # =========================================================

    def _has_christum_notation(self, value: str) -> bool:
        return (
                CHRISTUM_BC_PLACEHOLDER in value
                or CHRISTUM_AD_PLACEHOLDER in value
        )
