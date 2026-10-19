import os

from spacy.tokens import Span

from tests.validation.inp.inp_spacy_timespan import InpSpacyOutputFile
from tests.validation.timespan_utils import extract_year


class InpTensOutputFile(InpSpacyOutputFile):
    @staticmethod
    def write_header(filename: str) -> None:
        path = InpSpacyOutputFile.get_output_path(filename)
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
        InpTensOutputFile.write_timespan_entry(filename, entity.text, gateway)

    @staticmethod
    def write_timespan_entry(
        filename: str,
        entity_text: str,
        gateway=None,
    ):
        with open(
            InpSpacyOutputFile.get_output_path(filename), "a", encoding="utf-8"
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
