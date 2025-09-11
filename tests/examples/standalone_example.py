from pathlib import Path

from temporal_normalization import (
    close_conn,
    console,
    extract_temporal_expressions,
    start_conn,
    TemporalExpression,
)

LANG = "ro"
TEXT_RO = (
    "Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
    "În secolul XX, tehnologia a avansat semnificativ. "
    "Sec. 21 este adesea asociat cu globalizarea rapidă."
)

if __name__ == "__main__":
    # Display a warning if the language of the text is not Romanian.
    console.lang_warning(TEXT_RO, target_lang=LANG)

    root_path = str(Path(__file__).resolve().parent.parent.parent)
    java_process, gateway = start_conn(root_path)
    expressions: list[TemporalExpression] = extract_temporal_expressions(
        gateway, TEXT_RO
    )
    close_conn(java_process, gateway)

    for expression in expressions:
        for time_series in expression.time_series:
            edges = time_series.edges

            print("Start Edge:")
            print(edges.start.serialize("\t"))
            print()

            print("End Edge:")
            print(edges.end.serialize("\t"))
            print()

            print("Periods:")
            for period in time_series.periods:
                print(period.serialize("\t"))
                print()
            print("---------------------")
