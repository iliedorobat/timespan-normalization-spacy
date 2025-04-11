import spacy_stanza
import stanza

from normalizer.commons.print_utils import console
from normalizer.index import create_normalized_component, TemporalNormalization  ## noqa: F401

LANG = "ro"
TEXT_RO = ("Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
           "În secolul XX, tehnologia a avansat semnificativ. "
           "Sec. 21 este adesea asociat cu globalizarea rapidă.")

if __name__ == "__main__":
    # Display a warning if the language of the text is not Romanian.
    console.lang_warning(TEXT_RO, target_lang=LANG)

    try:
        # Load the Romanian pre-trained Stanza pipeline into the spaCy framework if already exists
        nlp = spacy_stanza.load_pipeline(LANG, download_method=None)
    except FileNotFoundError:
        console.warning(f'Started downloading the model for "{LANG}" language...')
        # Download the Romanian pre-trained Stanza pipeline only if it doesn't exist
        stanza.download(LANG)
        # Load the Romanian pre-trained Stanza pipeline into the spaCy framework
        nlp = spacy_stanza.load_pipeline(LANG)

    # Add "temporal_normalization" component to the spaCy pipeline
    nlp.add_pipe("temporal_normalization", last=True)
    doc = nlp(TEXT_RO)

    # Display NLP-specific linguistic annotations
    console.tokens_table(doc)
    print()

    # Display information about the identified and normalized dates in the text.
    for entity in doc.ents:
        if entity._.normalized:
            for edge in entity._.normalized.edges:
                print(edge.serialize())
                print()

            print("Periods:")
            for period in entity._.normalized.periods:
                print(period.serialize("\t"))
                print()
