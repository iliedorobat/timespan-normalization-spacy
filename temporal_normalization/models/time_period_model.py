from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import regex

from temporal_normalization.commons_temporal import (
    CHRISTUM_AD_PLACEHOLDER,
    CHRISTUM_BC_LABEL,
    CHRISTUM_BC_PLACEHOLDER,
    DBPEDIA_MILLENNIUM_PLACEHOLDER,
    DBPEDIA_CENTURY_PLACEHOLDER,
    get_ordinal,
    TemporalType,
    UNDERSCORE_PLACEHOLDER,
)
from temporal_normalization.commons_temporal.time_period_utils import (
    sanitize_time_period_interval,
    sanitize_time_period,
)
from temporal_normalization.models.dbpedia_model import DBpediaModel
from temporal_normalization.models.time_model import TimeModel
from temporal_normalization.rules import CENTURY_INTERVAL_PREFIXED, MILLENNIUM_INTERVAL_PREFIXED
from temporal_normalization.rules.year import YEAR_OR_SEPARATOR, YEAR_INTERVAL_PREFIXED

INTERVAL_PREFIXES = [
    CENTURY_INTERVAL_PREFIXED,
    MILLENNIUM_INTERVAL_PREFIXED,
    YEAR_INTERVAL_PREFIXED,
]


@dataclass
class TimePeriodModel(TimeModel):
    """
    Equivalent of Java TimePeriodModel extending TimeModel.
    """

    # =========================================================
    # Equivalent of Java default constructor
    # =========================================================
    def __post_init__(self):
        super().__init__()

    # =========================================================
    # toString()
    # =========================================================

    def __str__(self) -> str:
        time_period_set: Set[str] = set()

        millennium_set = self.get_millennium_set(
            self.era_start,
            self.era_end,
            self.millennium_start,
            self.millennium_end,
            True,
        )

        century_set = self.get_century_set(
            self.era_start,
            self.era_end,
            self.century_start,
            self.century_end,
            True,
        )

        year_set = self.get_year_set(
            self.era_start,
            self.era_end,
            self.year_start,
            self.year_end,
            False,
        )

        time_period_set.update(millennium_set)
        time_period_set.update(century_set)
        time_period_set.update(year_set)

        return DBpediaModel.tree_set_to_dbpedia_string(time_period_set)

    # =========================================================
    # DBpedia URI mapping
    # =========================================================

    def to_dbpedia_start_uri(self, matched_type: str) -> Optional[str]:
        if matched_type is None:
            return None

        if matched_type == TemporalType.CENTURY.value:
            return DBpediaModel.prepare_uri(self.era_start, self.century_start, matched_type)

        if matched_type == TemporalType.MILLENNIUM.value:
            return DBpediaModel.prepare_uri(self.era_start, self.millennium_start, matched_type)

        if matched_type in (TemporalType.DATE.value, TemporalType.YEAR.value):
            return DBpediaModel.prepare_uri(self.era_start, self.year_start, matched_type)

        return None

    def to_dbpedia_end_uri(self, matched_type: str) -> Optional[str]:
        if matched_type is None:
            return None

        if matched_type == TemporalType.CENTURY.value:
            return DBpediaModel.prepare_uri(self.era_end, self.century_end, matched_type)

        if matched_type == TemporalType.MILLENNIUM.value:
            return DBpediaModel.prepare_uri(self.era_end, self.millennium_end, matched_type)

        if matched_type in (TemporalType.DATE.value, TemporalType.YEAR.value):
            return DBpediaModel.prepare_uri(self.era_end, self.year_end, matched_type)

        return None

    def prepare_value(self, value: str, regex_str: str) -> str:
        if regex_str in INTERVAL_PREFIXES:
            return sanitize_time_period_interval(value)

        # TODO: check if this guard can be used for all INTERVAL_PREFIXES
        prepared_value = regex.sub(YEAR_OR_SEPARATOR, " - ", value, flags=regex.IGNORECASE) \
            if regex_str == YEAR_INTERVAL_PREFIXED \
            else value

        return sanitize_time_period(prepared_value)

    # =========================================================
    # Set builders
    # =========================================================

    @staticmethod
    def get_millennium_set(
            era_start: str,
            era_end: str,
            millennium_start: Optional[int],
            millennium_end: Optional[int],
            ordinal: bool,
    ) -> Set[str]:
        return TimePeriodModel.get_timeperiod_set(
            era_start,
            era_end,
            millennium_start,
            millennium_end,
            DBPEDIA_MILLENNIUM_PLACEHOLDER,
            ordinal,
        )

    @staticmethod
    def get_century_set(
            era_start: str,
            era_end: str,
            century_start: Optional[int],
            century_end: Optional[int],
            ordinal: bool,
    ) -> Set[str]:
        return TimePeriodModel.get_timeperiod_set(
            era_start,
            era_end,
            century_start,
            century_end,
            DBPEDIA_CENTURY_PLACEHOLDER,
            ordinal,
        )

    @staticmethod
    def get_year_set(
            era_start: str,
            era_end: str,
            year_start: Optional[int],
            year_end: Optional[int],
            ordinal: bool,
    ) -> Set[str]:
        return TimePeriodModel.get_timeperiod_set(
            era_start,
            era_end,
            year_start,
            year_end,
            "",
            ordinal,
        )

    # =========================================================
    # Core generator
    # =========================================================

    @staticmethod
    def get_timeperiod_set(
            era_start: str,
            era_end: str,
            start: Optional[int],
            end: Optional[int],
            time_placeholder: str,
            ordinal: bool,
    ) -> Set[str]:
        result: Set[str] = set()

        if start is None or end is None:
            return result

        TimePeriodModel._push_same_bc(
            era_start, era_end, start, end, time_placeholder, result, ordinal
        )
        TimePeriodModel._push_same_ad(
            era_start, era_end, start, end, time_placeholder, result, ordinal
        )
        TimePeriodModel._push_bc_ad(
            era_start, era_end, start, end, time_placeholder, result, ordinal
        )
        TimePeriodModel._push_ad_bc(
            era_start, era_end, start, end, time_placeholder, result, ordinal
        )

        return result

    # =========================================================
    # SAME AD
    # =========================================================

    @staticmethod
    def _push_same_ad(
            era_start: str,
            era_end: str,
            time_start: int,
            time_end: int,
            time_placeholder: str,
            time_set: Set[str],
            ordinal: bool,
    ):
        """
        Push a time period where the starting era and the ending era are both
        CHRISTUM_AD_PLACEHOLDER
        """
        if (
                era_start == CHRISTUM_AD_PLACEHOLDER
                and era_end == CHRISTUM_AD_PLACEHOLDER
        ):
            start = min(time_start, time_end)
            end = max(time_start, time_end)

            for time_period in range(start, end + 1):
                period = (
                    get_ordinal(time_period).ordinal
                    if ordinal
                    else str(time_period)
                )
                time_set.add(period + time_placeholder)

    # =========================================================
    # SAME BC
    # =========================================================

    @staticmethod
    def _push_same_bc(
            era_start: str,
            era_end: str,
            time_start: int,
            time_end: int,
            time_placeholder: str,
            time_set: Set[str],
            ordinal: bool,
    ):
        """
        Push a time period where the starting era and the ending era are both
        CHRISTUM_BC_PLACEHOLDER
        """
        if (
                era_start == CHRISTUM_BC_PLACEHOLDER
                and era_end == CHRISTUM_BC_PLACEHOLDER
        ):
            start = max(time_start, time_end)
            end = min(time_start, time_end)

            for time_period in range(start, end - 1, -1):
                period = (
                    get_ordinal(time_period).ordinal
                    if ordinal
                    else str(time_period)
                )

                time_set.add(
                    period
                    + time_placeholder
                    + UNDERSCORE_PLACEHOLDER
                    + CHRISTUM_BC_LABEL
                )

    # =========================================================
    # BC → AD
    # =========================================================

    @staticmethod
    def _push_bc_ad(
            era_start: str,
            era_end: str,
            time_start: int,
            time_end: int,
            time_placeholder: str,
            time_set: Set[str],
            ordinal: bool,
    ):
        if (
                era_start == CHRISTUM_BC_PLACEHOLDER
                and era_end == CHRISTUM_AD_PLACEHOLDER
        ):
            TimePeriodModel._push_same_bc(
                CHRISTUM_BC_PLACEHOLDER,
                CHRISTUM_BC_PLACEHOLDER,
                time_start,
                1,
                time_placeholder,
                time_set,
                ordinal,
            )

            TimePeriodModel._push_same_ad(
                CHRISTUM_AD_PLACEHOLDER,
                CHRISTUM_AD_PLACEHOLDER,
                1,
                time_end,
                time_placeholder,
                time_set,
                ordinal,
            )

    # =========================================================
    # AD → BC
    # =========================================================

    @staticmethod
    def _push_ad_bc(
            era_start: str,
            era_end: str,
            time_start: int,
            time_end: int,
            time_placeholder: str,
            time_set: Set[str],
            ordinal: bool,
    ):
        if (
                era_start == CHRISTUM_AD_PLACEHOLDER
                and era_end == CHRISTUM_BC_PLACEHOLDER
        ):
            TimePeriodModel._push_same_bc(
                CHRISTUM_BC_PLACEHOLDER,
                CHRISTUM_BC_PLACEHOLDER,
                time_end,
                1,
                time_placeholder,
                time_set,
                ordinal,
            )

            TimePeriodModel._push_same_ad(
                CHRISTUM_AD_PLACEHOLDER,
                CHRISTUM_AD_PLACEHOLDER,
                1,
                time_start,
                time_placeholder,
                time_set,
                ordinal,
            )
