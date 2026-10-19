import os

from spacy.tokens import Span

from temporal_normalization import TimeSeries


class InpInputFile:
    @staticmethod
    def get_input_path(dataset_type: str) -> str:
        path = f"{os.getcwd()}/tests/validation/files/input/timespan_{dataset_type}.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    @staticmethod
    def read_file(dataset_type: str) -> list[str]:
        with open(
            InpInputFile.get_input_path(dataset_type), "r", encoding="utf-8"
        ) as input_file:
            content = input_file.read()
            return content.split("\n")


class InpSpacyOutputFile:
    @staticmethod
    def get_output_path(filename: str) -> str:
        path = f"{os.getcwd()}/tests/validation/files/output/inp_{filename}.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    @staticmethod
    def write_header(filename: str) -> None:
        path = InpSpacyOutputFile.get_output_path(filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as csv_file:
            entry = "|".join(
                [
                    "input value",
                    "prepared value",
                    "normalized edge values",
                    "normalized values",
                ]
            )
            csv_file.write(entry + "\n")

    @staticmethod
    def write_empty_entry(
        filename: str,
        entity_text: str,
    ):
        with open(
            InpSpacyOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            entry = "|".join(
                [
                    entity_text,
                    entity_text,
                    "[]",
                    "[]",
                ]
            )
            csv_file.write(entry + "\n")

    @staticmethod
    def write_entity_entries(filename: str, entity: Span):
        if isinstance(entity._.time_series, list):
            for entry in entity._.time_series:
                InpSpacyOutputFile.write_timespan_entry(filename, entry)
        else:
            InpSpacyOutputFile.write_empty_entry(filename, entity.text)

    @staticmethod
    def write_timespan_entry(
        filename: str,
        time_series: TimeSeries,
    ):
        with open(
            InpSpacyOutputFile.get_output_path(filename), "a", encoding="utf-8"
        ) as csv_file:
            entry = "|".join(
                [
                    time_series.input_value,
                    time_series.prepared_value,
                    f"[{{start={time_series.edges.start.uri}, end={time_series.edges.end.uri}}}]",
                    _list_to_string([period.uri for period in time_series.periods]),
                ]
            )
            csv_file.write(entry + "\n")


def _list_to_string(input_list: list[str]) -> str:
    output = "["

    for item in input_list:
        if output != "[":
            output += ", "
        output += item

    output += "]"

    return output
