import os
from pathlib import Path

from spacy.tokens import Span, Doc

from temporal_normalization import TimeSeries
from tests.validation.ronec_types import Ronec, RonecTimespan


class RonecOutputFile:
    @staticmethod
    def get_output_path(filename: str) -> str:
        path = f"{str(Path(__file__).resolve().parent)}/files/output/{filename}.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    @staticmethod
    def write_entities_entries(
        filename: str, ronec_entry: Ronec, ronec_timespan: RonecTimespan, doc: Doc
    ):
        counter = 0

        for entity in doc.ents:
            RonecOutputFile.write_entity_entries(
                filename, ronec_entry, ronec_timespan, entity
            )
            counter += 1

        if counter == 0:
            RonecOutputFile.write_empty_entry(
                filename, ronec_entry, ronec_timespan, None
            )

    @staticmethod
    def write_entity_entries(
        filename: str,
        ronec_entry: Ronec,
        ronec_timespan: RonecTimespan,
        entity: Span,
    ) -> None:
        time_series = entity._.time_series

        if isinstance(time_series, list):
            for ts in time_series:
                if isinstance(ts, TimeSeries):
                    RonecOutputFile.write_timespan_entry(
                        filename, ronec_entry, ronec_timespan, entity.text, ts
                    )
                else:
                    RonecOutputFile.write_empty_entry(
                        filename, ronec_entry, ronec_timespan, entity.text
                    )
        else:
            RonecOutputFile.write_empty_entry(
                filename, ronec_entry, ronec_timespan, entity.text
            )

    @staticmethod
    def write_header(filename: str) -> None:
        with open(
            RonecOutputFile.get_output_path(filename), "w", encoding="utf-8"
        ) as csv_file:
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
            csv_file.write(entry + "\n")

    @staticmethod
    def write_empty_entry(
        filename: str,
        ronec_entry: Ronec,
        ronec_timespan: RonecTimespan | None,
        entity_text: str | None,
    ) -> None:
        with open(
            RonecOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            entry = "|".join(
                [
                    str(ronec_entry.sent["id"]),
                    ronec_entry.text,
                    ronec_timespan.text if ronec_timespan is not None else "",
                    ronec_timespan.tag_type.value if ronec_timespan is not None else "",
                    entity_text if entity_text is not None else "",
                    "",
                    "",
                    "",
                ]
            )
            csv_file.write(entry + "\n")

    @staticmethod
    def write_timespan_entry(
        filename: str,
        ronec_entry: Ronec,
        ronec_timespan: RonecTimespan,
        entity_text: str,
        time_series: TimeSeries | None,
    ) -> None:
        with open(
            RonecOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            entry = "|".join(
                [
                    str(ronec_entry.sent["id"]),
                    ronec_entry.text,
                    ronec_timespan.text,
                    ronec_timespan.tag_type.value,
                    entity_text,
                    " ## ".join(time_series.matches) if time_series is not None else "",
                    time_series.edges.start.label if time_series is not None else "",
                    time_series.edges.end.label if time_series is not None else "",
                ]
            )
            csv_file.write(entry + "\n")
