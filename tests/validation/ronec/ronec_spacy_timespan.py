from spacy.tokens import Span, Doc

from temporal_normalization import TimeSeries
from tests.validation.ronec.ronec_tens_timespan import RonecTensOutputFile
from tests.validation.ronec.ronec_types import Ronec, RonecTimespan
from tests.validation.timespan_utils import extract_year


class RonecSpacyOutputFile(RonecTensOutputFile):
    @staticmethod
    def write_entities_entries(
        filename: str, ronec_entry: Ronec, ronec_timespan: RonecTimespan, doc: Doc, gateway=None
    ):
        counter = 0

        for entity in doc.ents:
            RonecSpacyOutputFile.write_entity_entries(
                filename, ronec_entry, ronec_timespan, entity, gateway
            )
            counter += 1

        if counter == 0:
            RonecSpacyOutputFile.write_empty_entry(
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
            RonecSpacyOutputFile.write_timespan_entry(
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
            RonecSpacyOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            start, end, matches = extract_year(entity_text, gateway)
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
