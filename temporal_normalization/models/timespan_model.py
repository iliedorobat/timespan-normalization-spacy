from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Set, List

from temporal_normalization import TemporalType
from temporal_normalization.commons import EMPTY_VALUE_PLACEHOLDER
from temporal_normalization.models.dbpedia_model import DBpediaModel
from temporal_normalization.models.time_period_model import TimePeriodModel


@dataclass
class TimespanModel:
    residual_value: str = EMPTY_VALUE_PLACEHOLDER
    dbpedia_edges: Dict[str, DBpediaModel] = field(default_factory=dict)
    dbpedia_items: Set[DBpediaModel] = field(default_factory=set)

    def __init__(
            self,
            time_period: TimePeriodModel,
            matched_list: List[str],
            matched_value: str,
            matched_type: TemporalType,
            residual_value: str,
    ):
        self.residual_value = residual_value or EMPTY_VALUE_PLACEHOLDER
        self.dbpedia_edges = {}
        self.dbpedia_items = set()

        # TODO: pass matched_type instead of matched_type.value
        self.set_dbpedia_edges(time_period, matched_type.value, matched_value)
        self.set_dbpedia_items(matched_list, matched_type.value, matched_value)

    # =========================================================
    # getters (optional in Python, kept for parity)
    # =========================================================

    def get_dbpedia_edges(self) -> Dict[str, DBpediaModel]:
        return self.dbpedia_edges

    def get_dbpedia_items(self) -> Set[DBpediaModel]:
        return self.dbpedia_items

    def get_residual_value(self) -> str:
        return self.residual_value

    def set_dbpedia_edges(
            self,
            time_period: TimePeriodModel,
            matched_type: str,
            matched_value: str,
    ):
        edges: Dict[str, DBpediaModel] = {}

        start_uri = time_period.to_dbpedia_start_uri(matched_type)
        end_uri = time_period.to_dbpedia_end_uri(matched_type)

        # E.g.: "începutul mil.al XX-lea"
        if start_uri is None or end_uri is None:
            return

        start = DBpediaModel(start_uri, matched_type, matched_value)
        end = DBpediaModel(end_uri, matched_type, matched_value)

        edges["start"] = start
        edges["end"] = end

        self.dbpedia_edges = edges

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

        self.dbpedia_items.update(items)

    def set_residual_value(self, residual_value: str):
        self.residual_value = residual_value
