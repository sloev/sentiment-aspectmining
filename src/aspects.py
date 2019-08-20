import spacy

from src.udpipe import annotate as udpipe_annotate


def _danish_extractor(sentence):
    tokens = annotate(sentence, "da")
    return [t["word"] for t in tokens if t["pos"] == "NOUN"]


def _create_spacy_aspect_extractor(model_name):
    nlp = spacy.load(model_name)

    def extractor(sentence):
        doc = nlp(sentence)
        return [token.text for token in doc if token.pos_ == "NOUN"]

    return extractor


_aspect_extractors = {
    "da": _danish_extractor,
    "en": _create_spacy_aspect_extractor("en_core_web_sm"),
}


def extract_aspects(sentence, language, lower=True):
    aspect_extractor = _aspect_extractors[language]
    if lower:
        sentence = sentence.lower()
    return aspect_extractor(sentence)
