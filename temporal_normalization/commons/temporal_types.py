from enum import Enum


# TODO: merge with timespan_types
class TemporalType(Enum):
    CENTURY = "century"
    DATE = "date"
    EPOCH = "epoch"
    MILLENNIUM = "millennium"
    UNKNOWN = "unknown"
    YEAR = "year"
