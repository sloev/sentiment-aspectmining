from tqdm import tqdm
from src import aspects, sentences, reviews


def reviews_to_aspect_rows(review_generator):
    for review in tqdm(review_generator):
        review_text = review.pop("review_text")
        language = review["language"]
        rows = []
        for sentence in sentences.extract_sentences(review_text, language):
            for aspect in aspects.extract_aspects(sentence, language):
                review["aspect"] = aspect
                rows.append(dict(**review))
        yield rows


def process_bq():
    import json

    reviews_gen = reviews.generate_reviews("en", "5331df2f000064000578743c")
    for aspect_rows in reviews_to_aspect_rows(reviews_gen):
        for row in aspect_rows:
            print(json.dumps(row))
