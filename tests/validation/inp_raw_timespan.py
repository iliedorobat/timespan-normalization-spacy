import os

from spacy.tokens import Span

from tests.validation.inp_timespan import InpOutputFile
from tests.validation.normalization.utils import extract_year


class InpRawOutputFile(InpOutputFile):
    @staticmethod
    def write_header(filename: str) -> None:
        path = InpOutputFile.get_output_path(filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as csv_file:
            entry = "|".join(
                [
                    "input value",
                    "matches",
                    "start",
                    "end",
                ]
            )
            csv_file.write(entry + "\n")

    @staticmethod
    def write_entity_entries(filename: str, entity: Span, gateway=None):
        InpRawOutputFile.write_timespan_entry(filename, entity.text, gateway)

    @staticmethod
    def write_timespan_entry(
        filename: str,
        entity_text: str,
        gateway=None,
    ):
        with open(
            InpOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            start, end, matches = extract_year(entity_text, gateway)
            entry = "|".join(
                [
                    entity_text,
                    matches,
                    start,
                    end,
                ]
            )
            csv_file.write(entry + "\n")
