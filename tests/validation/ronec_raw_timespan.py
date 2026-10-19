from spacy.tokens import Span, Doc

from temporal_normalization import TemporalExpression, extract_temporal_expressions, TimeSeries
from tests.validation.ronec_timespan import RonecOutputFile
from tests.validation.ronec_types import Ronec, RonecTimespan


class RonecRawOutputFile(RonecOutputFile):
    @staticmethod
    def write_entities_entries(
        filename: str, ronec_entry: Ronec, ronec_timespan: RonecTimespan, doc: Doc, gateway=None
    ):
        counter = 0

        for entity in doc.ents:
            RonecRawOutputFile.write_entity_entries(
                filename, ronec_entry, ronec_timespan, entity, gateway
            )
            counter += 1

        if counter == 0:
            RonecRawOutputFile.write_empty_entry(
                filename, ronec_entry, ronec_timespan, None
            )
    @staticmethod
    def write_entity_entries(
        filename: str,
        ronec_entry: Ronec,
        ronec_timespan: RonecTimespan,
        entity: Span,
        gateway=None
    ) -> None:
        if entity.label_ in ["DATETIME", "PERIOD"]:
            RonecRawOutputFile.write_timespan_entry(
                filename, ronec_entry, ronec_timespan, entity.text, None, gateway
            )

    @staticmethod
    def write_timespan_entry(
        filename: str,
        ronec_entry: Ronec,
        ronec_timespan: RonecTimespan,
        entity_text: str,
        time_series: TimeSeries | None,
        gateway=None,
    ) -> None:
        with open(
            RonecRawOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            start, end, matches = _extract_year(entity_text, gateway)
            entry = "|".join(
                [
                    str(ronec_entry.sent["id"]),
                    ronec_entry.text,
                    ronec_timespan.text,
                    ronec_timespan.tag_type.value,
                    entity_text,
                    matches,
                    start,
                    end,
                ]
            )
            csv_file.write(entry + "\n")


def _extract_year(text: str, gateway) -> tuple[str, str, str]:
    try:
        expressions: list[TemporalExpression] = extract_temporal_expressions(
            gateway, text
        )

        if len(expressions) and len(expressions[0].time_series):
            edges = expressions[0].time_series[0].edges
            matches = expressions[0].matches
            start = edges.start.label
            end = edges.end.label

            return start, end, " ## ".join(matches)

        return text, text, text
    except Exception as e:
        print(f"Error: {e}")
        return text, text, text
