import subprocess

import spacy
from spacy import Language

from temporal_normalization import console
from temporal_normalization.index import (
    create_normalized_component,  # noqa: F401
    TemporalNormalization,  # noqa: F401
)


def load_model(model_name: str) -> Language:
    """
    Loads a spaCy language model by name, downloading it if necessary,
    and adds the ``temporal_normalization`` pipeline component.

    Args:
        model_name (str): The name of the spaCy model to load (e.g., ``ro_core_news_sm``).

    Returns:
        Language: The loaded spaCy language model with the temporal normalization component added.

    Example:
        >>> nlp = load_model("ro_core_news_sm")
        >>> doc = nlp("În 1962 , SUA instituie blocada economică asupra Cubei .")
        >>> print(doc)

    Notes:
        - If the model is not already downloaded, this function will download it automatically.
        - The ``temporal_normalization`` component is appended to the pipeline.
    """

    try:
        # Load the spaCy model if it has already been downloaded
        nlp = spacy.load(model_name)
    except OSError:
        console.warning(f"Started downloading {model_name}...")
        # Download the Romanian model if it wasn't already downloaded
        subprocess.run(["python", "-m", "spacy", "download", model_name])
        # Load the spaCy model
        nlp = spacy.load(model_name)

    # Add "temporal_normalization" component to the spaCy pipeline
    nlp.add_pipe("temporal_normalization", last=True)

    return nlp
