from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from temporal_normalization.commons_temporal import (
    CHRISTUM_BC_LABEL,
    CHRISTUM_BC_PLACEHOLDER,
    DBPEDIA_CENTURY_PLACEHOLDER,
    DBPEDIA_MILLENNIUM_PLACEHOLDER,
    get_ordinal,
    NS_DBPEDIA_RESOURCE,
    STRING_LIST_SEPARATOR,
    TemporalType,
    UNDERSCORE_PLACEHOLDER,
)


@dataclass
class DBpediaModel:
    """
    A model representing an entity from DBpedia, storing key attributes related
    to the entity.

    Attributes:
        uri (str): The unique identifier (URI) of the DBpedia entity.
        matched_value (str): The original matched value from the input data.
        matched_type (TemporalType or None): The temporal type of the entity,
            if applicable.
        label (str): A human-readable name for the entity.
    """

    uri: str = None
    matched_type: TemporalType = None
    matched_value: str = None
    label: Optional[str] = None

    def __init__(self, uri: str, matched_type: str, matched_value: str):
        self.uri = uri
        self.matched_type = TemporalType(matched_type)
        self.matched_value = matched_value
        self.label = (uri.replace(NS_DBPEDIA_RESOURCE, "")
                      .replace(UNDERSCORE_PLACEHOLDER, " "))

    def __repr__(self):
        return f"DBpediaModel(label={self.label}, uri={self.uri})"

    def serialize(self, indent: str = ""):
        matched_type = self.matched_type.value if self.matched_type else None

        return (
            f"{indent}Matched value: {self.matched_value}\n"
            f"{indent}Matched Type: {matched_type}\n"
            f"{indent}Normalized label: {self.label}\n"
            f"{indent}DBpedia uri: {self.uri}"
        )

    @staticmethod
    def prepare_uri(era: str, value: Optional[int], matched_type: str) -> Optional[str]:
        """
        Convert an integer time unit into a DBpedia URI.

        E.g.: "1/2 mil. 5 - sec. i al mil. 4 a.chr."
        E.g.: "09 1875"
        """
        if value is None:
            return None

        if matched_type == TemporalType.CENTURY.value:
            return (
                    NS_DBPEDIA_RESOURCE
                    + get_ordinal(value).ordinal
                    + DBPEDIA_CENTURY_PLACEHOLDER
                    + DBpediaModel._get_era_suffix(era)
            )

        if matched_type == TemporalType.MILLENNIUM.value:
            return (
                    NS_DBPEDIA_RESOURCE
                    + get_ordinal(value).ordinal
                    + DBPEDIA_MILLENNIUM_PLACEHOLDER
                    + DBpediaModel._get_era_suffix(era)
            )

        if matched_type in (TemporalType.DATE.value, TemporalType.YEAR.value):
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

    @staticmethod
    def _get_era_suffix(value: str) -> str:
        return (
            UNDERSCORE_PLACEHOLDER + CHRISTUM_BC_LABEL
            if value and CHRISTUM_BC_PLACEHOLDER in value
            else ""
        )

    # =========================================================
    # Python dunder methods
    # =========================================================

    # TODO: check whether dunder methods are necessary
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
