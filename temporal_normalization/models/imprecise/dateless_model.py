from __future__ import annotations

import re
from dataclasses import dataclass

from temporal_normalization.models.year_model import YearModel
from temporal_normalization.rules import REGEX_OR
from temporal_normalization.rules.imprecise import DATELESS_MODEL_X, DATELESS_UNDATED
from temporal_normalization.rules.year import YEAR_INTERVAL_BASE, YEAR_INTERVAL_PREFIXED, YEAR_OPTIONS


@dataclass
class DatelessModel(YearModel):
    """
    Model pentru expresii de tip 'dateless' (fără an explicit complet),
    unde anul este dedus din pattern-uri alternative.
    """

    PATTERN: str = rf"({YEAR_INTERVAL_PREFIXED}){REGEX_OR}({YEAR_INTERVAL_BASE})"

    def __init__(self, original: str, value: str, regex: str, historical_only: bool):
        super().__init__()

        self.original = original
        self.value = value
        self.regex = regex
        self.historical_only = historical_only

        # logic direct aici (fără __post_init__)
        self._apply_dateless_logic()

    def _apply_dateless_logic(self) -> None:
        if self.regex not in (DATELESS_MODEL_X, DATELESS_UNDATED):
            return

        match = re.search(self.PATTERN, self.original)
        if match:
            self.set_year_model(
                self.original,
                match.group(),
                self.regex,
                self.historical_only,
            )
            return

        match = re.search(YEAR_OPTIONS, self.original)
        if match:
            self.set_year_model(
                self.original,
                match.group(),
                self.regex,
                self.historical_only,
            )
