from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set, List, Optional

from temporal_normalization.commons_temporal import EMPTY_VALUE_PLACEHOLDER, TemporalType
from temporal_normalization.models.dbpedia_model import DBpediaModel
from temporal_normalization.models.time_period_model import TimePeriodModel


@dataclass
class EdgeModel:
    """
    A model representing time interval represented as DBpedia entities.
    This edge represents the starting and ending points of a time period.

    Attributes:
        start (DBpediaModel): The starting entity of the time period.
        end (DBpediaModel): The ending entity of the time period.
    """

    start: Optional[DBpediaModel] = None
    end: Optional[DBpediaModel] = None

    def __repr__(self):
        return f"EdgeModel(start={self.start}, end={self.end})"

    def serialize(self, indent: str = ""):
        start = self.start.serialize("\t")
        end = self.end.serialize("\t")

        return f"{indent}Start time:\n{start}\n" f"{indent}End time:\n{end}"


@dataclass
class TimespanModel:
    residual_value: str = EMPTY_VALUE_PLACEHOLDER
    edges: EdgeModel = field(default_factory=EdgeModel())
    periods: Set[DBpediaModel] = field(default_factory=set)

    def __init__(
            self,
            time_period: TimePeriodModel,
            matched_list: List[str],
            matched_value: str,
            matched_type: TemporalType,
            residual_value: str,
    ):
        self.residual_value = residual_value or EMPTY_VALUE_PLACEHOLDER
        self.edges = EdgeModel()
        self.periods = set()

        # TODO: pass matched_type instead of matched_type.value
        self.set_dbpedia_edges(time_period, matched_type.value, matched_value)
        self.set_dbpedia_items(matched_list, matched_type.value, matched_value)

    # =========================================================
    # getters (optional in Python, kept for parity)
    # =========================================================

    def get_dbpedia_edges(self) -> EdgeModel:
        return self.edges

    def get_dbpedia_items(self) -> Set[DBpediaModel]:
        return self.periods

    def get_residual_value(self) -> str:
        return self.residual_value

    def set_dbpedia_edges(
            self,
            time_period: TimePeriodModel,
            matched_type: str,
            matched_value: str,
    ):
        start_uri = time_period.to_dbpedia_start_uri(matched_type)
        end_uri = time_period.to_dbpedia_end_uri(matched_type)

        # E.g.: "începutul mil.al XX-lea"
        if start_uri is None or end_uri is None:
            return

        start = DBpediaModel(start_uri, matched_type, matched_value)
        end = DBpediaModel(end_uri, matched_type, matched_value)

        self.edges = EdgeModel(start, end)

    def set_dbpedia_items(
            self,
            matched_list: List[str],
            matched_type: str,
            matched_value: str,
    ):
        items = {
            DBpediaModel(uri, matched_type, matched_value)
            for uri in matched_list
        }

        self.periods.update(items)

    def set_residual_value(self, residual_value: str):
        self.residual_value = residual_value
