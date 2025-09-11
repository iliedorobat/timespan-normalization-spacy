from temporal_normalization import console, TemporalExpression, start_process

LANG = "ro"
TEXT_RO = (
    "Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
    "În secolul XX, tehnologia a avansat semnificativ. "
    "Sec. 21 este adesea asociat cu globalizarea rapidă."
)

if __name__ == "__main__":
    # Display a warning if the language of the text is not Romanian.
    console.lang_warning(TEXT_RO, target_lang=LANG)

    expressions: list[TemporalExpression] = []
    start_process(TEXT_RO, expressions)

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
