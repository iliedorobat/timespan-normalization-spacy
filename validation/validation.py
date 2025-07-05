from functools import total_ordering

from datasets import load_dataset

from mock.mock_data import ronec_example
from model import load_model
from ronec_timespan import Ronec, OutputFile

LANG = "ro"
MODEL = "ro_core_news_sm"


def validate_dataset(dataset_type: str, mock_data: bool = False):
    """
    Runs a validation loop over a specified dataset (e.g., ``validation``, ``test``, or ``train``),
    applying a spaCy model to all temporal expressions and writing the results to file.

    The function loads RONEC entries, extracts their associated timespans (temporal expressions),
    processes each using the NLP model, and writes the annotated output using ``OutputFile``.

    Args:
        dataset_type (str): The name of the dataset split to validate. Expected values:
                            ``validation``, ``test``, and ``train``.
        mock_data (bool): Whether to use a mocked example dataset (useful for testing).
                          Defaults to False.

    Example:
        >>> validate_dataset("validation")
        >>> validate_dataset("test")
        >>> validate_dataset("train", mock_data=True)

    Prints:
        - Number of total entries in the dataset.
        - Number of entries containing at least one timespan.
        - Total number of individual temporal expressions processed.

    Note:
        This function assumes that:
            - ``load_model``, ``load_dataset``, ``Ronec``, and ``OutputFile`` are correctly defined and imported.
            - ``ronec_example`` is a valid mock RONEC object when ``mock_data=True``.
    """

    nlp = load_model(MODEL)

    ronec = ronec_example if mock_data else load_dataset("ronec")
    OutputFile.write_header(dataset_type)
    dataset = ronec[dataset_type]
    total_rows = 0
    total_timespans = 0

    print(f"{dataset_type}: no. of entries = {len(dataset)}")

    for i, item in enumerate(dataset):
        ronec_entry = Ronec(ronec, dataset_type, item)

        if ronec_entry.timespans:
            print(f"i = {i}")
            total_rows += 1
            local_counter = 0

            for timespan in ronec_entry.timespans:
                doc = nlp(timespan.text)
                local_counter += OutputFile.write_entities_entries(dataset_type, ronec_entry, timespan, doc)
                total_timespans += 1

            if local_counter == 0:
                OutputFile.write_empty_entry(dataset_type, ronec_entry, None, None)

    print(f"{dataset_type}: no. of date and periods entries = {total_rows}")
    print(f"{dataset_type}: TOTAL no. of date and periods = {total_timespans}")


if __name__ == "__main__":
    pass
