__author__ = "jgv@trustpilot.com"
__version__ = "0.0.1"

from src.udpipe.models import load_model


def annotate(text, language):
    model = load_model(language)
    sentences = model.tokenize(text)
    tokens = []
    for s in sentences:
        model.tag(s)
        model.parse(s)

        for word in s.words:
            if word.form == "<root>":
                continue
            tokens.append(dict(word=word.form, lemma=word.lemma, pos=word.upostag))
    return tokens
