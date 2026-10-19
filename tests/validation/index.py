from enum import Enum
from pathlib import Path

from datasets import load_dataset

from inp_timespan import InpInputFile, InpOutputFile
from ronec_timespan import Ronec, RonecOutputFile
from temporal_normalization import start_conn, close_conn
from tests.model import load_model
from tests.validation.inp_raw_timespan import InpRawOutputFile
from tests.validation.ronec_mock_data import ronec_example
from tests.validation.ronec_raw_timespan import RonecRawOutputFile

MODEL = "ro_core_news_sm"


class PipelineType(Enum):
    SPACY = "spacy"
    TENS = "tens"


# print(nlp.get_pipe("ner").labels)
def validate_ronec_corpus(dataset_type: str, pipeline_type: PipelineType=PipelineType.TENS, mock_data: bool=False):
    """
    Runs a validation loop over a specified dataset (e.g., ``validation``, ``test``,
    or ``train``), applying a spaCy model to all temporal expressions and writing the
    results to file.

    The function loads RONEC entries, extracts their associated timespans (temporal
    expressions), processes each using the NLP model, and writes the annotated output
    using ``OutputFile``.

    Args:
        dataset_type (str): The name of the dataset split to validate. Expected values:
                            ``validation``, ``test``, and ``train``.
        pipeline_type (PipelineType): Type of the pipeline. Expected values: ``spacy``,
                            and ``tens``
        mock_data (bool): Whether to use a mocked example dataset (useful for testing).
                          Defaults to False.

    Example:
        >>> validate_ronec_corpus("validation")
        >>> validate_ronec_corpus("test")
        >>> validate_ronec_corpus("train", mock_data=True)

    Prints:
        - Number of total entries in the dataset.
        - Number of entries containing at least one timespan.
        - Total number of individual temporal expressions processed.

    Note:
        This function assumes that:
            - ``load_model``, ``load_dataset``, ``Ronec``, and ``OutputFile`` are correctly defined and imported.
            - ``ronec_example`` is a valid mock RONEC object when ``mock_data=True``.
    """

    include_pipeline = pipeline_type == PipelineType.TENS
    nlp = load_model(MODEL, include_pipeline)

    # Start gateway once for SPACY pipeline
    java_process = None
    gateway = None
    if pipeline_type == PipelineType.SPACY:
        root_path = str(Path(__file__).resolve().parent.parent.parent)
        java_process, gateway = start_conn(root_path)

    try:
        ronec = ronec_example if mock_data else load_dataset("ronec")
        if pipeline_type == PipelineType.SPACY:
            RonecRawOutputFile.write_header(dataset_type + "_raw")
        elif pipeline_type == PipelineType.TENS:
            RonecOutputFile.write_header(dataset_type)
        dataset = ronec[dataset_type]
        total_rows = 0
        total_timespans = 0

        print(f"{dataset_type}: no. of entries = {len(dataset)}")

        for i, item in enumerate(dataset):
            ronec_entry = Ronec(ronec, dataset_type, item)

            if ronec_entry.timespans:
                print(f"i = {i}")
                total_rows += 1

                for timespan in ronec_entry.timespans:
                    doc = nlp(timespan.text)
                    if pipeline_type == PipelineType.SPACY:
                        RonecRawOutputFile.write_entities_entries(dataset_type + "_raw", ronec_entry, timespan, doc, gateway)
                    elif pipeline_type == PipelineType.TENS:
                        RonecOutputFile.write_entities_entries(dataset_type, ronec_entry, timespan, doc)
                    total_timespans += 1

        print(f"{dataset_type}: no. of date and periods entries = {total_rows}")
        print(f"{dataset_type}: TOTAL no. of date and periods = {total_timespans}")
    finally:
        # Close the gateway once at the end
        if pipeline_type == PipelineType.SPACY:
            try:
                close_conn(java_process, gateway)
            except Exception:
                pass


def validate_inp_data(dataset_type: str, pipeline_type: PipelineType=PipelineType.TENS):
    include_pipeline = pipeline_type == PipelineType.TENS
    nlp = load_model(MODEL, include_pipeline)

    # Start gateway once for SPACY pipeline
    java_process = None
    gateway = None
    if pipeline_type == PipelineType.SPACY:
        root_path = str(Path(__file__).resolve().parent.parent.parent)
        java_process, gateway = start_conn(root_path)

    if pipeline_type == PipelineType.SPACY:
        InpRawOutputFile.write_header(dataset_type + "_raw")
    elif pipeline_type == PipelineType.TENS:
        InpOutputFile.write_header(dataset_type)
    raw_timespans = InpInputFile.read_file(dataset_type)

    try:
        for raw_timespan in raw_timespans:
            doc = nlp(raw_timespan)

            for entity in doc.ents:
                if pipeline_type == PipelineType.SPACY:
                    InpRawOutputFile.write_entity_entries(dataset_type + "_raw", entity, gateway)
                elif pipeline_type == PipelineType.TENS:
                    InpOutputFile.write_entity_entries(dataset_type, entity)
    finally:
        # Close the gateway once at the end
        if pipeline_type == PipelineType.SPACY:
            try:
                close_conn(java_process, gateway)
            except Exception:
                pass


if __name__ == "__main__":
    validate_ronec_corpus("validation", PipelineType.SPACY)
    validate_ronec_corpus("test", PipelineType.SPACY)

    validate_ronec_corpus("validation", PipelineType.TENS)
    validate_ronec_corpus("test", PipelineType.TENS)

    validate_inp_data("additional", PipelineType.SPACY)
    validate_inp_data("additional", PipelineType.TENS)

    validate_inp_data("unique", PipelineType.SPACY)
    validate_inp_data("unique", PipelineType.TENS)

    # # validate_inp_data("all", PipelineType.SPACY)
    # # validate_inp_data("all", PipelineType.TENS)
