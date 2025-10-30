from temporal_normalization.commons.print_utils import console
from tests.model import load_model

LANG = "ro"
MODEL = "ro_core_news_sm"
TEXT_RO = (
    "Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
    "În secolul XX, tehnologia a avansat semnificativ. "
    "Sec. 21 este adesea asociat cu globalizarea rapidă."
)

if __name__ == "__main__":
    # Display a warning if the language of the text is not Romanian.
    console.lang_warning(TEXT_RO, target_lang=LANG)

    nlp = load_model(MODEL)
    doc = nlp(TEXT_RO)

    # Display NLP-specific linguistic annotations
    console.tokens_table(doc)
    print()

    # Display information about the identified and normalized dates in the text.
    for entity in doc.ents:
        time_series = entity._.time_series

        if isinstance(time_series, list):
            for ts in time_series:
                edges = ts.edges

                print("Start Edge:")
                print(edges.start.serialize("\t"))
                print()

                print("End Edge:")
                print(edges.end.serialize("\t"))
                print()

                print("Periods:")
                for period in ts.periods:
                    print(period.serialize("\t"))
                    print()
                print("---------------------")
