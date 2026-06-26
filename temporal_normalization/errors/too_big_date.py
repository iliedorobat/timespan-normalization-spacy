from __future__ import annotations

import sys


class TooBigDateUnitError(RuntimeError):
    """
    Base error for invalid temporal values in a given context.
    """

    unit_name: str = ""

    def __init__(self, operation: str, position: str, value: int):
        self.operation = operation
        self.position = position
        self.value = value

        super().__init__(self.get_message(operation, position, value))

    @classmethod
    def get_message(cls, operation: str, position: str, value: int) -> str:
        return (
            f"{operation}: The {position} {cls.unit_name} ({value}) "
            f"is not valid in the current context."
        )

    @classmethod
    def print_message(cls, operation: str, position: str, value: int) -> None:
        print(cls.get_message(operation, position, value), file=sys.stderr)


class TooBigYearError(TooBigDateUnitError):
    unit_name = "year"

    @property
    def year(self) -> int:
        return self.value


class TooBigCenturyError(TooBigDateUnitError):
    unit_name = "century"

    @property
    def century(self) -> int:
        return self.value


class TooBigMillenniumError(TooBigDateUnitError):
    unit_name = "millennium"

    @property
    def millennium(self) -> int:
        return self.value
