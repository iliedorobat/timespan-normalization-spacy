import re
import unicodedata

from spacy import Language
from spacy.tokens import Doc, Span

from normalizer.commons.temporal_models import TemporalExpression
from normalizer.process.java_process import start_process

try:
    @Language.factory("temporal_normalization")
    def create_normalized_component(nlp, name):
        return TemporalNormalization(nlp, name)
except AttributeError:
    # spaCy 2.x
    pass


class TemporalNormalization:
    __FIELD = "normalized"

    def __init__(self, nlp: Language, name: str):
        Span.set_extension("normalized", default=None, force=True)
        self.nlp = nlp

    def __call__(self, doc: Doc) -> Doc:
        expressions: list[TemporalExpression] = []
        start_process(doc, expressions, "normalizer/process/")
        str_matches: list[str] = _prepare_str_patterns(expressions)

        new_ents = _find_dates(doc, str_matches, expressions)
        doc.set_ents(list(doc.ents) + new_ents)

        return doc


def _prepare_str_patterns(expressions: list[TemporalExpression]) -> list[str]:
    matches: list[str] = []

    for expression in expressions:
        for match in expression.matches:
            matches.append(match)

    return matches


def _find_dates(doc: Doc, str_matches: list[str], expressions: list[TemporalExpression]) -> list[Span]:
    regex_matches: list[str] = [fr"{item}" for item in str_matches]
    pattern = f"({'|'.join(regex_matches)})"
    matches = list(re.finditer(pattern, remove_accents(doc.text), re.IGNORECASE)) if len(regex_matches) > 0 else []
    new_ents = []

    for match in matches:
        start_char, end_char = match.start(), match.end()
        start_token, end_token = None, None

        for token in doc:
            if token.idx == start_char:
                start_token = token.i
            if token.idx + len(token.text) == end_char:
                end_token = token.i

        if start_token is not None and end_token is not None:
            entity = Span(doc, start_token, end_token + 1, label="DATE")
            expression = next((item for item in expressions if remove_accents(entity.text) in item.matches), None)

            if expression:
                entity._.set("normalized", expression)

            new_ents.append(entity)
        else:
            print(f"Warning: Could not find tokens for match '{match.group()}' at {start_char}-{end_char}")

    return new_ents


def remove_accents(input_str):
    # Normalize the input string to NFD form (decomposed)
    nfkd_form = unicodedata.normalize('NFD', input_str)
    # Filter out characters that are combining accents (category 'Mn' stands for Non-spacing Mark)
    return ''.join([c for c in nfkd_form if unicodedata.category(c) != 'Mn'])


if __name__ == "__main__":
    pass
