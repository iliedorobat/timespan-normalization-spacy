from enum import Enum

from datasets import DatasetDict, Dataset

from temporal_normalization import console

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


class RonecTimespan:
    def __init__(self, start: int, end: int, text: str, tag: str):
        self.start = start
        self.end = end
        self.text = text
        self.tag = tag
        self.tag_type = RonecTimespan.get_tag_type(tag)

    def __repr__(self):
        return f'Timespan(tag={self.tag}, text="{self.text}")'

    def append_text(self, end: int, text: str, tag: str) -> None:
        self.end = end
        self.text += EMPTY_SPACE + text

        tag_type = RonecTimespan.get_tag_type(tag)
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


def _get_timespans(tokens: list[str], tags: list[str]) -> list[RonecTimespan]:
    timespans = []
    timespan = None

    for i, tag in enumerate(tags):
        if tag == "B-PERIOD" or tag == "B-DATETIME":
            if isinstance(timespan, RonecTimespan):
                timespans.append(timespan)

            timespan = RonecTimespan(i, i, tokens[i], tag)
        elif tag == "I-PERIOD" or tag == "I-DATETIME":
            if isinstance(timespan, RonecTimespan):
                timespan.append_text(i, tokens[i], tag)
    else:
        if isinstance(timespan, RonecTimespan):
            timespans.append(timespan)

    return timespans
