from __future__ import annotations

import calendar
import re


class Date:
    """
    Equivalent of Java ro.webdata.echo.commons.Date utility class.
    """

    LAST_UPDATE_CENTURY = 21
    LAST_UPDATE_MILLENNIUM = 3
    LAST_UPDATE_YEAR = 2014

    UNKNOWN_MONTH = "Unknown"

    # =========================================================
    # prepareDate()
    # =========================================================
    @staticmethod
    def prepare_date(value: str) -> str:
        return value.replace(",", "").strip()

    # =========================================================
    # getMonthName()
    # =========================================================
    @staticmethod
    def get_month_name(month: str) -> str:
        month_number = -1

        try:
            month_number = int(month)
        except ValueError:
            month_number = Date._map_month_to_number(month)

        return Date._map_number_to_month(month_number, month)

    # =========================================================
    # mapNumberToMonth()
    # =========================================================
    @staticmethod
    def _map_number_to_month(month_number: int, month_name: str) -> str:
        try:
            if 1 <= month_number <= 12:
                return calendar.month_name[month_number]
        except Exception:
            pass

        # mimic UnknownMonthException.printMessage behavior
        print(f"Unknown month: {month_number} ({month_name})")

        return Date.UNKNOWN_MONTH

    # =========================================================
    # mapMonthToNumber()
    # =========================================================
    @staticmethod
    def _map_month_to_number(month: str) -> int:
        value = re.sub(r"\.", "", month).lower().strip()

        if value.startswith(("jan", "ian")):
            return 1

        if value.startswith("feb") or value == "fevruarie":
            return 2

        if value.startswith("mar"):
            return 3

        if value.startswith("apr"):
            return 4

        if value in ("may", "mai"):
            return 5

        if (
                value.startswith("jun")
                or value.startswith("iun")
                or value == "iumie"
        ):
            return 6

        if value.startswith(("iul", "jul")):
            return 7

        if value.startswith("aug"):
            return 8

        if value.startswith("sep"):
            return 9

        if value.startswith("oct") or value.startswith("0ct"):
            return 10

        if value.startswith(("noi", "nov")):
            return 11

        if value.startswith("dec"):
            return 12

        return -1
