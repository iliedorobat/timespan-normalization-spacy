from enum import Enum


LAST_UPDATE_CENTURY = 21
LAST_UPDATE_MILLENNIUM = 3
LAST_UPDATE_YEAR = 2014


DBPEDIA_CENTURY_PLACEHOLDER = "_century"
DBPEDIA_MILLENNIUM_PLACEHOLDER = "_millennium"
EMPTY_VALUE_PLACEHOLDER = ""
UNDERSCORE_PLACEHOLDER = "_"
STRING_LIST_SEPARATOR = " ### "


NS_DBPEDIA_RESOURCE = "https://dbpedia.org/page/"


class TemporalType(Enum):
    CENTURY = "century"
    DATE = "date"
    EPOCH = "epoch"
    MILLENNIUM = "millennium"
    UNKNOWN = "unknown"
    YEAR = "year"


# TODO: remove
# Environment variables
PRINT_ERROR = True
