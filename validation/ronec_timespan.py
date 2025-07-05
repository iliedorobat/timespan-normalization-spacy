from enum import Enum

from datasets import DatasetDict, Dataset
from spacy.tokens import Span, Doc

from temporal_normalization import console, TimeSeries

EMPTY_SPACE = " "


class Ronec:
    def __init__(self, dataset_dict: DatasetDict, dataset_type: str, sent: Dataset):
        label_names = dataset_dict[dataset_type].features["ner_tags"].feature.names
        tags = [label_names[tag] for tag in sent["ner_tags"]]
        tokens = sent["tokens"]

        self.text = "".join(
            token + (EMPTY_SPACE if space else "")
            for token, space in zip(sent["tokens"], sent["space_after"])
        )
        self.timespans = _get_timespans(tokens, tags)
        self.sent = sent
        self.dataset_type = dataset_type

    def __repr__(self):
        return f"RonecMeta(sent_id={self.sent['id']}, timespans={self.timespans}, text=\"{self.text}\")"


class RonecTagType(Enum):
    DATETIME = "DATETIME"
    PERIOD = "PERIOD"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_


class Timespan:
    def __init__(self, start: int, end: int, text: str, tag: str):
        self.start = start
        self.end = end
        self.text = text
        self.tag = tag
        self.tag_type = Timespan.get_tag_type(tag)

    def __repr__(self):
        return f'Timespan(tag={self.tag}, text="{self.text}")'

    def append_text(self, end: int, text: str, tag: str) -> None:
        self.end = end
        self.text += EMPTY_SPACE + text

        tag_type = Timespan.get_tag_type(tag)
        if self.tag_type != tag_type:
            console.warning(f"tag_type={self.tag_type} but received {tag_type}.")

    @staticmethod
    def get_tag_type(tag: str) -> RonecTagType | None:
        tag_type = tag[2:]

        if not RonecTagType.has_value(tag_type):
            console.error(
                f"tag_type={tag_type} is not a valid tag type.\nPlease use {RonecTagType.DATETIME.value} or {RonecTagType.PERIOD.value}."
            )
            return None

        return RonecTagType._value2member_map_.get(tag_type)


class OutputFile:
    @staticmethod
    def get_output_path(dataset_type: str) -> str:
        return f"validation/output_{dataset_type}.csv"

    @staticmethod
    def write_entities_entries(
        dataset_type: str, ronec_entry: Ronec, ronec_timespan: Timespan, doc: Doc
    ):
        for entity in doc.ents:
            OutputFile.write_entity_entries(
                dataset_type, ronec_entry, ronec_timespan, entity
            )

    @staticmethod
    def write_entity_entries(
        dataset_type: str, ronec_entry: Ronec, ronec_timespan: Timespan, entity: Span
    ) -> None:
        time_series = entity._.time_series

        if isinstance(time_series, list):
            for ts in time_series:
                if isinstance(ts, TimeSeries):
                    OutputFile.write_timespan_entry(
                        dataset_type, ronec_entry, ronec_timespan, entity.text, ts
                    )
                else:
                    OutputFile.write_empty_entry(dataset_type, ronec_entry, ronec_timespan, entity.text)
        else:
            OutputFile.write_empty_entry(dataset_type, ronec_entry, ronec_timespan, entity.text)

    @staticmethod
    def write_header(dataset_type: str) -> None:
        with open(
            OutputFile.get_output_path(dataset_type), "w", encoding="utf-8"
        ) as csvfile:
            entry = "|".join(
                [
                    "id",
                    "sentence",
                    "ronec timespan",
                    "tag_type",
                    "spacy entity",
                    "matches",
                    "start",
                    "end",
                ]
            )
            csvfile.write(entry + "\n")

    @staticmethod
    def write_empty_entry(
        dataset_type: str, ronec_entry: Ronec, ronec_timespan: Timespan, entity_text: str
    ) -> None:
        with open(
            OutputFile.get_output_path(dataset_type), "a", encoding="utf-8"
        ) as csvfile:
            entry = "|".join(
                [
                    str(ronec_entry.sent["id"]),
                    ronec_entry.text,
                    ronec_timespan.text,
                    ronec_timespan.tag_type.value,
                    entity_text,
                    "",
                    "",
                    "",
                ]
            )
            csvfile.write(entry + "\n")

    @staticmethod
    def write_timespan_entry(
        dataset_type: str,
        ronec_entry: Ronec,
        ronec_timespan: Timespan,
        entity_text: str,
        time_series: TimeSeries,
    ) -> None:
        with open(
            OutputFile.get_output_path(dataset_type), "a", encoding="utf-8"
        ) as csvfile:
            entry = "|".join(
                [
                    str(ronec_entry.sent["id"]),
                    ronec_entry.text,
                    ronec_timespan.text,
                    ronec_timespan.tag_type.value,
                    entity_text,
                    " ## ".join(time_series.matches),
                    time_series.edges.start.label,
                    time_series.edges.end.label,
                ]
            )
            csvfile.write(entry + "\n")


def _get_timespans(tokens: list[str], tags: list[str]) -> list[Timespan]:
    timespans = []
    timespan = None

    for i, tag in enumerate(tags):
        if tag == "B-PERIOD" or tag == "B-DATETIME":
            if isinstance(timespan, Timespan):
                timespans.append(timespan)

            timespan = Timespan(i, i, tokens[i], tag)
        elif tag == "I-PERIOD" or tag == "I-DATETIME":
            if isinstance(timespan, Timespan):
                timespan.append_text(i, tokens[i], tag)
    else:
        if isinstance(timespan, Timespan):
            timespans.append(timespan)

    return timespans
