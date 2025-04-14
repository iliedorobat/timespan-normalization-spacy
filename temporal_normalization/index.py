import re

from spacy import Language
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from temporal_normalization import TimeSeries
from temporal_normalization.commons.temporal_models import TemporalExpression
from temporal_normalization.process.java_process import start_process

try:

    @Language.factory("temporal_normalization")
    def create_normalized_component(nlp, name):
        return TemporalNormalization(nlp, name)

except AttributeError:
    # spaCy 2.x
    pass


class TemporalNormalization:
    __FIELD = "time_series"

    def __init__(self, nlp: Language, name: str):
        Span.set_extension(TemporalNormalization.__FIELD, default=None, force=True)
        self.nlp = nlp

    def __call__(self, doc: Doc) -> Doc:
        expressions: list[TemporalExpression] = []
        start_process(doc.text, expressions)
        str_matches: list[str] = _prepare_str_patterns(expressions)

        _retokenize(doc, str_matches, expressions)

        return doc


def _prepare_str_patterns(expressions: list[TemporalExpression]) -> list[str]:
    matches: list[str] = []

    for expression in expressions:
        for match in expression.matches:
            matches.append(match)

    return matches


def _retokenize(
    doc: Doc, str_matches: list[str], expressions: list[TemporalExpression]
) -> None:
    regex_matches: list[str] = [rf"{item}" for item in str_matches]
    pattern = f"({'|'.join(regex_matches)})"
    matches = (
        list(re.finditer(pattern, doc.text, re.IGNORECASE))
        if len(regex_matches) > 0
        else []
    )

    with doc.retokenize() as retokenizer:
        for match in matches:
            start_char, end_char = match.start(), match.end()
            start_token, end_token = None, None

            for token in doc:
                if token.idx == start_char:
                    start_token = token.i
                if token.idx + len(token.text) == end_char:
                    end_token = token.i

            if start_token is not None and end_token is not None:
                entity = Span(doc, start_token, end_token + 1, label="DATETIME")
                time_series: list[TimeSeries] = [ts for expression in expressions for ts in expression.time_series]
                expression: TimeSeries | None = next((ts for ts in time_series if entity.text in ts.matches), None)

                if expression:
                    entity._.set("time_series", expression)
                    # E.g.: "În secolul XX, tehnologia a avansat semnificativ."
                    all_ents = list(doc.ents) + [entity]
                    doc.ents = filter_spans(all_ents)

                retokenizer.merge(entity)
            else:
                print(
                    f"Warning: Could not find tokens for match '{match.group()}' "
                    f"at {start_char}-{end_char}"
                )


if __name__ == "__main__":
    pass
