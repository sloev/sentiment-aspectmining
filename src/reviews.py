import pandas as pd


def generate_reviews(language, business_unit_id=None, from_date=None, to_date=None):
    offset = 0
    limit = 10000
    query = """
        SELECT
            LOWER(Review_Text) as review_text,
            Review_id as review_id,
            Review_Language as language,
            Review_Created as created,
            Domain_id as business_unit_id
        FROM
        `datalake-restricted-production.sra.mongo_servicereviewsaggregator_servicereviewsaggregator_ReviewSimpleSummary` reviews
        WHERE {filters}
        ORDER BY Review_Created ASC
        LIMIT {limit}
        OFFSET {offset}
    """
    filters = [f"Review_Language = '{language}'"]
    if from_date:
        if to_date:
            filters.append(
                f"""
                EXTRACT(DATE FROM TIMESTAMP_MILLIS(CAST(Review_Created AS INT64))) >= '{from_date}'
                AND
                EXTRACT(DATE FROM TIMESTAMP_MILLIS(CAST(Review_Created AS INT64))) < '{to_date}'
            """
            )
        else:
            filters.append(
                f"""
                EXTRACT(DATE FROM TIMESTAMP_MILLIS(CAST(Review_Created AS INT64))) = '{from_date}'
            """
            )
    if business_unit_id:
        filters.append(f"Domain_id = '{business_unit_id}'")

    while True:
        df = pd.pandas.read_gbq(
            query=query.format(
                filters=" AND ".join(filters), limit=limit, offset=offset
            ),
            project_id="datalake-datamarts-production",
            dialect="standard",
        )
        for index, row in df.iterrows():
            row = dict(row)
            yield row

        if len(df) < limit:
            break
        offset += limit
