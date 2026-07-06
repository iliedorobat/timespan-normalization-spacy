from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set

from temporal_normalization.commons_temporal import normalize_christum_notation
from temporal_normalization.commons_temporal.time_sanitize_utils import sanitize_value
from temporal_normalization.commons_temporal.timespan_utils import prepare_timespan_models
from temporal_normalization.models import TimespanModel, DBpediaModel, EdgeModel


# FIXME:
#  nedatat (1852 ? – 1860 ?)
#  an 1  an 21  etc.
#  1/2 mil. 5 - sec. I al mil. 4 a.Chr.
#  2 a.chr - 14 p.chr


@dataclass
class TimeExpression:
    SEPARATOR = "|"

    prepared_value: str = ""
    input_value: str = ""
    timespan_models: List[TimespanModel] = field(default_factory=list)

    @staticmethod
    def get_headers() -> str:
        headers = [
            "input value",
            "prepared value",
            "normalized edge values",
            "normalized values",
        ]

        return TimeExpression.SEPARATOR.join(headers)

    def __init__(
            self,
            input_value: str,
            historical_only: bool = False,
            sanitize: bool = False,
    ):
        """
        Set the original value, the value whose Christum notation has been
        sanitized and the prepared value (the DBpedia links)

        @param input_value The original value
        @param historical_only Flag which specifies whether the Framework will only handle
                               historical dates (future dates will be ignored)
        @param sanitize Flag specifying if the custom method sanitize_value
                        will be used to sanitize values. Use True only if you use this
                        framework on LIDO datasets.
        """
        try:
            # TODO: handle the case when input_value is None
            sanitized_value = (
                sanitize_value(input_value)
                if sanitize
                else input_value
            )

            self.input_value = input_value
            self.prepared_value = normalize_christum_notation(
                sanitized_value
            )
            self.timespan_models = prepare_timespan_models(
                input_value,
                historical_only,
                sanitize,
            )

        except Exception:
            print(
                "Something went wrong while creating the "
                '"TimeExpression" object with the following parameters:'
                f"\n\tinput_value = {input_value}"
                f"\n\thistorical_only = {historical_only}"
                f"\n\tsanitize = {sanitize}"
            )

            import traceback
            traceback.print_exc()

            self.input_value = input_value
            self.prepared_value = ""
            self.timespan_models = []

    def __str__(self) -> str:
        return (
            f"{self.input_value}"
            f"{self.SEPARATOR}{self.prepared_value}"
            f"{self.SEPARATOR}{self.get_dbpedia_edges()}"
            f"{self.SEPARATOR}{self.get_dbpedia_items()}"
        )

    def serialize(self) -> str:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
            default=str,
        )

    def get_dbpedia_edges(self) -> List[Dict[str, DBpediaModel]]:
        edges: List[Dict[str, DBpediaModel]] = []

        for timespan_model in self.timespan_models:
            edges.append(timespan_model.get_dbpedia_edges())

        return edges

    def get_dbpedia_items(self) -> Set[DBpediaModel]:
        items: Set[DBpediaModel] = set()

        for timespan_model in self.timespan_models:
            items.update(timespan_model.get_dbpedia_items())

        return items


class TemporalExpression:
    """
    A model representing a temporal expression, extracted and processed.

    Attributes:
        is_valid (bool): A flag that specifies whether the text processed
            through timespan-normalization library is a temporal expression.
        input_value (str or None): The original temporal expression before processing.
        prepared_value (str or None): The temporal expression after processing.
        time_series (list[TimeSeries]): The list of normalized temporal expressions.
        matches (list[str]): A unique list of matched values found in the normalized
            entities.
    """

    def __init__(self, time_expression: TimeExpression):
        # TODO: remove is_valid flag (used for the validating deserialized Java objects)
        self.is_valid = time_expression.input_value is not None and isinstance(time_expression.timespan_models, list)
        self.input_value = time_expression.input_value
        self.prepared_value = time_expression.prepared_value
        self.time_series: list[TimeSeries] = [
            TimeSeries(item) for item in time_expression.timespan_models
        ] if self.is_valid else []
        self.matches: list[str] = list(
            set(
                [
                    matched_value
                    for ts in self.time_series
                    for matched_value in ts.matches
                ]
            )
        )

    def __str__(self):
        if self.input_value is None:
            return "TemporalExpression(None)"

        return f"TemporalExpression({self.input_value})"

    def __repr__(self):
        return self.input_value


class TimeSeries:
    """
    A data structure representing a temporal expression that has been normalized
    into a list of periods and temporal edges.

    Attributes:
        edges (list[EdgeModel]): A list of temporal intervals represented as edges.
        periods (list[DBpediaModel]): A list of normalized DBpedia entities
            extracted from the expression.
        matches (list[str]): A unique list of matched values found in the normalized
            entities.
    """

    def __init__(self, timespan: TimespanModel):
        self.edges: EdgeModel = timespan.edges
        self.periods: set[DBpediaModel] = timespan.periods
        self.matches: list[str] = list(
            set([item.matched_value for item in self.periods])
        )

    def __repr__(self):
        return f"TimeSeries(edges={self.edges}, periods={self.periods})"

    def serialize(self, indent: str = ""):
        # fmt: off
        return (
            f"{indent}Edges: {self.edges}\n"
            f"{indent}Periods: {self.periods}"
        )
        # fmt: on


def extract_temporal_expressions(time_expression: TimeExpression):
    """
    Extracts valid temporal expressions from the given TimeExpression object.

    Args:
        time_expression (TimeExpression): Input from which to extract temporal
            expressions.

    Returns:
        list[TemporalExpression]: A list containing valid temporal expressions.
    """

    expressions: list[TemporalExpression] = []
    temporal_expression = TemporalExpression(time_expression)

    if temporal_expression.is_valid:
        expressions.append(temporal_expression)

    return expressions
