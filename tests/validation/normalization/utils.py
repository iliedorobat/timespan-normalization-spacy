from temporal_normalization import TemporalExpression, extract_temporal_expressions


def extract_year(text: str, gateway) -> tuple[str, str, str]:
    try:
        expressions: list[TemporalExpression] = extract_temporal_expressions(
            gateway, text
        )

        if len(expressions) and len(expressions[0].time_series):
            edges = expressions[0].time_series[0].edges
            matches = expressions[0].matches
            start = edges.start.label
            end = edges.end.label

            return start, end, " ## ".join(matches)

        return text, text, text
    except Exception as e:
        print(f"Error: {e}")
        return text, text, text
