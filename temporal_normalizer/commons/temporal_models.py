import json
from py4j.java_gateway import JavaObject

from temporal_normalizer.commons.temporal_types import TemporalType


class TemporalExpression:
    """
    A model representing a temporal expression, extracted and processed from a Java object.

    Attributes:
        is_valid (bool): A flag that specifies whether the text processed through timespan-normalization library is a temporal expression.
        initial (str or None): The original temporal expression before processing.
        edges (list[EdgeModel]): A list of temporal intervals represented as edges.
        periods (list[DBpediaModel]): A list of normalized DBpedia entities extracted from the expression.
        matches (list[str]): A unique list of matched values found in the normalized entities.
    """

    def __init__(self, java_object: JavaObject):
        serialize = java_object.serialize()
        json_obj = json.loads(serialize)

        self.is_valid = TemporalExpression.is_valid_json(json_obj)
        self.initial: str | None = json_obj["initial"] if self.is_valid else None
        self.edges: list[EdgeModel] = [
            EdgeModel(item) for item in json_obj["edges"]
        ] if self.is_valid else []
        self.periods: list[DBpediaModel] = [
            DBpediaModel(item) for item in json_obj["periods"]
        ] if self.is_valid else []
        self.matches: list[str] = list(
            set(
                [item.matched_value for item in self.periods]
            )
        )

    def __str__(self):
        if self.initial is None:
            return "TemporalExpression(None)"

        return f"TemporalExpression({self.initial})"

    def __repr__(self):
        return self.initial

    @staticmethod
    def is_valid_json(json_obj) -> bool:
        return ("initial" in json_obj
                and "edges" in json_obj
                and "periods" in json_obj)


class DBpediaModel:
    """
    A model representing an entity from DBpedia, storing key attributes related to the entity.

    Attributes:
        uri (str): The unique identifier (URI) of the DBpedia entity.
        label (str): A human-readable name for the entity.
        matched_value (str): The original matched value from the input data.
        matched_type (TemporalType or None): The temporal type of the entity, if applicable.
    """

    def __init__(self, data: dict):
        self.uri: str = data["uri"] if "uri" in data else None
        self.label: str = data["label"] if "label" in data else None
        self.matched_value: str = data["matchedValue"] if "matchedValue" in data else None
        try:
            self.matched_type: TemporalType = TemporalType(data["matchedType"]) if "matchedType" in data else None
        except ValueError:
            self.matched_type = None

    def __repr__(self):
        return f"DBpediaModel(label={self.label}, matched_value={self.matched_value})"

    def serialize(self, indent: str = ""):
        return (f"{indent}Matched value: {self.matched_value}\n"
                f"{indent}Matched Type: {self.matched_type.value if self.matched_type else None}\n"
                f"{indent}Normalized label: {self.label}\n"
                f"{indent}DBpedia uri: {self.uri}")


class EdgeModel:
    """
    A model representing time interval represented as DBpedia entities.
    This edge represents the starting and ending points of a time period.

    Attributes:
        start (DBpediaModel): The starting entity of the time period.
        end (DBpediaModel): The ending entity of the time period.
    """

    def __init__(self, data: dict):
        self.start: DBpediaModel = DBpediaModel(data["start"]) if "start" in data else None
        self.end: DBpediaModel = DBpediaModel(data["end"]) if "end" in data else None

    def __repr__(self):
        return f"EdgeModel(start={self.start}, end={self.end})"

    def serialize(self, indent: str = ""):
        start = self.start.serialize("\t")
        end = self.end.serialize("\t")

        return (f"{indent}Start time:\n{start}\n"
                f"{indent}End time:\n{end}")
