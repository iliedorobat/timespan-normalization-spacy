from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from temporal_normalization.commons import CHRISTUM_BC_LABEL, CHRISTUM_BC_PLACEHOLDER, get_ordinal
from temporal_normalization.commons_temporal.constants import (
    DBPEDIA_CENTURY_PLACEHOLDER,
    DBPEDIA_MILLENNIUM_PLACEHOLDER,
    UNDERSCORE_PLACEHOLDER,
    NS_DBPEDIA_RESOURCE,
    STRING_LIST_SEPARATOR,
)
from temporal_normalization.commons_temporal.timespan_types import CENTURY_TYPE, MILLENNIUM_TYPE, DATE_TYPE, YEAR_TYPE


@dataclass
class DBpediaModel:
    uri: Optional[str] = None
    label: Optional[str] = None
    matched_value: Optional[str] = None
    matched_type: Optional[str] = None

    # =========================================================
    # Equivalent of Java constructor logic
    # =========================================================
    def __post_init__(self):
        if self.uri is not None:
            self.label = (
                self.uri.replace(NS_DBPEDIA_RESOURCE, "")
                .replace(UNDERSCORE_PLACEHOLDER, " ")
            )

    # =========================================================
    # prepareUri()
    # =========================================================

    @staticmethod
    def prepare_uri(era: str, value: Optional[int], matched_type: str) -> Optional[str]:
        """
        Convert an integer time unit into a DBpedia URI.

        E.g.: "1/2 mil. 5 - sec. i al mil. 4 a.chr."
        E.g.: "09 1875"
        """
        if value is None:
            return None

        if matched_type == CENTURY_TYPE:
            return (
                    NS_DBPEDIA_RESOURCE
                    + get_ordinal(value).ordinal
                    + DBPEDIA_CENTURY_PLACEHOLDER
                    + DBpediaModel._get_era_suffix(era)
            )

        if matched_type == MILLENNIUM_TYPE:
            return (
                    NS_DBPEDIA_RESOURCE
                    + get_ordinal(value).ordinal
                    + DBPEDIA_MILLENNIUM_PLACEHOLDER
                    + DBpediaModel._get_era_suffix(era)
            )

        if matched_type in (DATE_TYPE, YEAR_TYPE):
            return (
                    NS_DBPEDIA_RESOURCE
                    + str(value)
                    + DBpediaModel._get_era_suffix(era)
            )

        return None

    @staticmethod
    def tree_set_to_dbpedia_string(tree_set):
        return STRING_LIST_SEPARATOR.join(
            f"{NS_DBPEDIA_RESOURCE}{item}"
            for item in sorted(tree_set)
        )

    # =========================================================
    # Python dunder methods
    # =========================================================

    def __str__(self) -> str:
        return self.uri

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True

        if not isinstance(other, DBpediaModel):
            return False

        return self.uri == other.uri

    def __hash__(self) -> int:
        return hash(self.uri) + hash(self.matched_value)

    # =========================================================
    # Era suffix helper
    # =========================================================

    @staticmethod
    def _get_era_suffix(value: str) -> str:
        return (
            UNDERSCORE_PLACEHOLDER + CHRISTUM_BC_LABEL
            if value and CHRISTUM_BC_PLACEHOLDER in value
            else ""
        )
