from __future__ import annotations

from dataclasses import dataclass

from temporal_normalization.models.time_period_model import TimePeriodModel
from temporal_normalization.rules import (
    AURIGNACIAN_CULTURE,
    BRONZE_AGE,
    CHALCOLITHIC_AGE,
    FRENCH_CONSULATE_AGE,
    HALLSTATT_CULTURE,
    INTERWAR_PERIOD,
    MIDDLE_AGES,
    MESOLITHIC_AGE,
    MODERN_AGES,
    NEOLITHIC_AGE,
    NERVA_ANTONINE_DYNASTY,
    PLEISTOCENE_AGE,
    PTOLEMAIC_DYNASTY,
    RENAISSANCE,
    ROMAN_EMPIRE_AGE,
    WW_I_PERIOD,
    WW_II_PERIOD,
)


@dataclass
class AgeModel(TimePeriodModel):
    age: str = None

    # =========================================================
    # Constructor equivalent
    # =========================================================
    def __init__(self, original: str, age: str, regex: str, historical_only: bool):
        super().__init__()

        self.age = self._map_age(age, regex)

        # Java intentionally passes null values
        self.set_millennium(original, None, None, historical_only)
        self.set_century(original, None, None, historical_only)

    # =========================================================
    # mapAge()
    # =========================================================

    def _map_age(self, age: str, regex: str) -> str:
        """
        Map regex-based age identifiers to DB-friendly labels.
        """

        if regex == AURIGNACIAN_CULTURE:
            return "Aurignacian"

        if regex == BRONZE_AGE:
            return "Bronze_Age"

        if regex == CHALCOLITHIC_AGE:
            return "Chalcolithic"

        if regex == FRENCH_CONSULATE_AGE:
            return "French_Consulate"

        if regex == HALLSTATT_CULTURE:
            return "Hallstatt_culture"

        if regex == INTERWAR_PERIOD:
            return "Interwar_period"

        if regex == MIDDLE_AGES:
            return "Middle_Ages"

        if regex == MESOLITHIC_AGE:
            return "Mesolithic"

        if regex == MODERN_AGES:
            return "Modern_history"

        if regex == NEOLITHIC_AGE:
            return "Neolithic"

        if regex == NERVA_ANTONINE_DYNASTY:
            return "Nerva–Antonine_dynasty"

        if regex == PLEISTOCENE_AGE:
            return "Pleistocene"

        if regex == PTOLEMAIC_DYNASTY:
            return "Ptolemaic_dynasty"

        if regex == RENAISSANCE:
            return "Renaissance"

        if regex == ROMAN_EMPIRE_AGE:
            return "Roman_Empire"

        if regex == WW_I_PERIOD:
            return "World_War_I"

        if regex == WW_II_PERIOD:
            return "World_War_II"

        return age
