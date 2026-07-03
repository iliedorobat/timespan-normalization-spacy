from spacy import Language

from temporal_normalization import TemporalNormalization

try:
    @Language.factory("temporal_normalization")
    def create_component(nlp, name):
        return TemporalNormalization(nlp, name)
except AttributeError:
    # spaCy 2.x
    pass
