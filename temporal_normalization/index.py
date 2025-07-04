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
    """
    spaCy pipeline component for identifying and annotating temporal expressions in text.

    This component calls the ``start_process`` method to extract temporal expressions, then
    aligns the matches with spaCy tokens using retokenization and sets a custom attribute
    containing associated time series metadata.
    """

    __FIELD = "time_series"

    def __init__(self, nlp: Language, name: str):
        """
        Initialize the component and register a custom extension on spaCy spans.

        Args:
            nlp (Language): A spaCy language object.
            name (str): The name of the component (unused, but typically required by spaCy).
        """

        Span.set_extension(TemporalNormalization.__FIELD, default=None, force=True)
        self.nlp = nlp

    def __call__(self, doc: Doc) -> Doc:
        """
        Apply the component to a spaCy Doc object.

        Extracts temporal expressions from the text, retokenizes spans to align with
        matched expressions, and attaches time series data to those spans.

        Args:
            doc (Doc): The input spaCy Doc object.

        Returns:
            Doc: The modified Doc object with temporal expressions processed.
        """

        expressions: list[TemporalExpression] = []
        start_process(doc.text, expressions)
        str_matches: list[str] = _prepare_str_patterns(expressions)

        _retokenize(doc, str_matches, expressions)

        return doc


def _prepare_str_patterns(expressions: list[TemporalExpression]) -> list[str]:
    """
    Collect all string matches from a list of temporal expressions.

    Args:
        expressions (list[TemporalExpression]): The list of extracted temporal expressions.

    Returns:
        list[str]: All string matches found across expressions.
    """

    matches: list[str] = []

    for expression in expressions:
        for match in expression.matches:
            matches.append(match)

    return matches


def _retokenize(
    doc: Doc, str_matches: list[str], expressions: list[TemporalExpression]
) -> None:
    """
    Retokenizes the doc to align with matched temporal expressions and attaches
    time series metadata to the identified spans.

    Matches are found using regular expressions. If a valid span can be created
    from character offsets, the span is assigned a ``time_series`` extension and
    optionally added to the doc's entity list.

    Args:
        doc (Doc): The spaCy Doc to be modified.
        str_matches (list[str]): The raw text patterns matched from expressions.
        expressions (list[TemporalExpression]): Original extracted expressions,
                                                each with time series metadata.
    """

    regex_matches: list[str] = [rf"{item}" for item in str_matches]
    pattern = f"({'|'.join(regex_matches)})"
    matches = (
        list(re.finditer(pattern, doc.text, re.IGNORECASE))
        if len(regex_matches) > 0
        else []
    )

    with doc.retokenize() as retokenizer:
        for match in matches:
            if not isinstance(match, re.Match):
                print(f"Invalid match object: {match!r}")
                continue

            start_char, end_char = match.start(), match.end()
            start_token, end_token = None, None

            for token in doc:
                if token.idx == start_char:
                    start_token = token.i
                if token.idx + len(token.text) == end_char:
                    end_token = token.i

            if start_token is not None and end_token is not None:
                entity, exists = _create_span(doc, start_char, end_char, start_token, end_token)
                time_series: list[TimeSeries] = [ts for expression in expressions for ts in expression.time_series]
                matched_ts = [ts for ts in time_series if _matched(entity.text, ts.matches)]

                if len(matched_ts) > 0:
                    if exists:
                        entity._.time_series = matched_ts
                    else:
                        entity._.set("time_series", matched_ts)

                    all_ents = list(doc.ents)
                    if entity not in all_ents:
                        # E.g.: entity in all_ents => "Ecaterina Balș ( 22 iulie 1814 - august 1887 ) - născută în familia Dimachi , a doua soție a generalului Teodor Balș ( 1805-1857 ) , caimacam al Moldovei în perioada 1856-1857 , cu care se căsătorise la 30 iunie 1846 la Dimăcheni ( Dorohoi ) ."
                        # E.g.: entity not in all_ents => "În secolul XX, tehnologia a avansat semnificativ."
                        all_ents.append(entity)

                    doc.ents = filter_spans(all_ents)

                    if entity not in all_ents:
                        retokenizer.merge(entity)
            else:
                print(
                    f"Warning: Could not find tokens for match '{match.group()}' "
                    f"at {start_char}-{end_char}"
                )


def _matched(text: str, matches: list[str]) -> bool:
    """
    Checks if a given text segment matches any string in a list of patterns.

    Args:
        text (str): The span text to be checked.
        matches (list[str]): A list of raw string patterns.

    Returns:
        bool: True if any pattern is found in the text, otherwise False.
    """

    for match in matches:
        if match in text:
            return True

    return False


def _create_span(doc: Doc, start_char: int, end_char: int, start_token: int, end_token: int) -> tuple[Span, bool]:
    """
    Creates a new span for a temporal expression or returns an existing overlapping entity.

    Args:
        doc (Doc): The spaCy Doc object.
        start_char (int): Start character offset of the match.
        end_char (int): End character offset of the match.
        start_token (int): Index of the starting token.
        end_token (int): Index of the ending token.

    Returns:
        tuple[Span, bool]: A tuple containing the Span object and a flag indicating
                           whether the span already existed as an entity.
    """

    for ent in doc.ents:
        if ent.start_char <= start_char and ent.end_char >= end_char:
            return ent, True

    return Span(doc, start_token, end_token + 1, label="DATETIME"), False


if __name__ == "__main__":
    pass
