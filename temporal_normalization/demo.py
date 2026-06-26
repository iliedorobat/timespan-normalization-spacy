from temporal_normalization.time_expression import TimeExpression


# PATH_OUTPUT_ALL_TIMESPAN_FILE = (
#         Path(File.PATH_OUTPUT_DIR)
#         / f"timespan_all.{File.EXTENSION_TXT}"
# )


def main(args: list[str]) -> None:
    value = _get_value(args, "--expression")
    historical = _historical_only(args)
    sanitize_values = _sanitize(args)

    time_expression = TimeExpression(
        value,
        historical,
        sanitize_values,
    )

    print(time_expression.serialize())


# TODO: implement the analytics
# def print_unknown_time_expressions(input_full_path: str) -> None:
#     # 1779; TOTAL: 39427
#     _print_unknown_time_expressions(input_full_path)


def print_full_timespan(
        input_full_path: str,
        historical_only: bool,
        sanitize: bool,
) -> None:
    """
    Print the original value, the value whose Christum notation has been
    sanitized and the prepared value (the DBpedia links)

    !!! writeTimespan will be used to generate the required text files !!!

    @param input_full_path The full path to the text file
                           (E.g.: "timespan_all.txt")
                           which stores the timespan values
                           (E.g.: PATH_OUTPUT_ALL_TIMESPAN_FILE)
    @param historical_only Flag which specifies whether the Framework
                           will only handle historical dates
                           (future dates will be ignored)
    @param sanitize Flag specifying if the custom method
                    TimeSanitizeUtils.sanitize_value
                    will be used to sanitize values.
                    Use True only if you use this framework
                    on LIDO datasets.
    """
    try:
        with open(input_full_path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if line:
                    print(
                        TimeExpression(
                            line,
                            historical_only,
                            sanitize,
                        )
                    )

    except OSError:
        import traceback
        traceback.print_exc()


def _get_value(pairs: list[str], comparator: str) -> str | None:
    for pair in pairs:
        key, *values = pair.split("=", 1)

        if key == comparator:
            if values:
                # E.g.: --historicalOnly=true
                return values[0]

            # E.g.: --historicalOnly
            return "true"

    return None


def _historical_only(pairs: list[str]) -> bool:
    value = _get_value(pairs, "--historicalOnly")
    if value is None:
        return False
    return value.lower() == "true"


def _sanitize(pairs: list[str]) -> bool:
    value = _get_value(pairs, "--sanitize")
    if value is None:
        return False
    return value.lower() == "true"


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
