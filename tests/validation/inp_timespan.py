import os
from pathlib import Path

from temporal_normalization import TimeSeries


class InpInputFile:
    @staticmethod
    def get_input_path(dataset_type: str) -> str:
        path = f"{str(Path(__file__).resolve().parent)}/files/input/timespan_{dataset_type}.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    @staticmethod
    def read_file(dataset_type: str) -> list[str]:
        with open(
            InpInputFile.get_input_path(dataset_type), "r", encoding="utf-8"
        ) as input_file:
            content = input_file.read()
            return content.split("\n")


class InpOutputFile:
    @staticmethod
    def get_output_path(dataset_type: str) -> str:
        path = f"{str(Path(__file__).resolve().parent)}/files/output/inp_{dataset_type}.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    @staticmethod
    def write_header(dataset_type: str) -> None:
        path = InpOutputFile.get_output_path(dataset_type)
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
        dataset_type: str,
        entity_text: str,
    ):
        with open(
            InpOutputFile.get_output_path(dataset_type), "a", encoding="utf-8"
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
    def write_timespan_entry(
        dataset_type: str,
        time_series: TimeSeries,
    ):
        with open(
            InpOutputFile.get_output_path(dataset_type), "a", encoding="utf-8"
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
