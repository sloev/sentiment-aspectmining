from nltk.tokenize import sent_tokenize

_NLTK_LANGUAGE_CODES = {"da": "danish", "en": "english"}


def extract_sentences(review_text, language):
    return sent_tokenize(review_text, language=_NLTK_LANGUAGE_CODES[language])
