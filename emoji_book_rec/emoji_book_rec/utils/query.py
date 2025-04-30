""" query.py
    This module contains the function to process emoji queries and return book titles
    based on the keywords associated with the emojis."""

from collections import Counter
import pandas as pd

from .keyword_tsv_to_dict import generate_keyword_dict
from .index import create_index


def process_query(query, filepath, use_precomputed=True, matrix_path=None):
    """

        :param query: List of emoji queries from user in Unicode

        :param filepath: File path for emoji keyword list

        :param use_precomputed: If True, use a precomputed keyword-book matrix

    :param matrix_path: Required if use_precomputed=True; path to the TSV matrix

        :return: Sorted dictionary of book titles

    """

    # emoji_kw_dict: Dictionary of emojis and associated keywords
    emoji_kw_dict = generate_keyword_dict(filepath)

    # book index
    # kw_book_index = create_index(books, emoji_kw_dict)  # build index

    query_keywords = []

    for emoji in emoji_kw_dict:

        if emoji in query:
            query_keywords.extend(emoji_kw_dict[emoji])  # flatten list

    keyword_counts = Counter(query_keywords)

    # ----------------New logic----------------
    print(query_keywords)
    print(keyword_counts)

    if use_precomputed:

        if not matrix_path:
            raise ValueError("Matrix path required when use_precomputed=True")

        matrix_df = pd.read_csv(matrix_path, sep="\t", index_col=0)

        book_scores = {}

        # for kw, multiplier in keyword_counts.items():

        for kw, count in keyword_counts.items():

            if kw in matrix_df.index:

                for book_title, freq in matrix_df.loc[kw].items():
                    # book_scores[book_title] = book_scores.get(book_title, 0) + freq * multiplier
                    book_scores[book_title] = book_scores.get(book_title, 0) + freq * count

        for i, (key, value) in enumerate(sorted(book_scores.items(), key=lambda x: x[1], reverse=True)):
            if i >= 25:
                break
            print(f"Key: {key}, Value: {value}")

        return sorted(book_scores.items(), key=lambda x: x[1], reverse=True)

    # ----------------End of new logic----------------

    # Prioritize keywords appearing multiple times

    book_scores = {}

    for keyword, count in keyword_counts.items():

        for book_title, tf_count in kw_book_index.get(keyword, []):

            if book_title in book_scores:

                book_scores[book_title] += tf_count * count

            else:

                book_scores[book_title] = tf_count * count
