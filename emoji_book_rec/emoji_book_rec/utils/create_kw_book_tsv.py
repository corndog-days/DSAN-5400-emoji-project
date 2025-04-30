"""Create a keyword-book matrix from the emoji-keyword mapping and book descriptions.
This script generates a matrix where each row corresponds to a keyword (or its synonyms)"""

import pandas as pd
import numpy as np
from nltk.corpus import wordnet


def get_synonyms(word):
    """Get a set of synonyms for a word using WordNet.
    :param word: The word to find synonyms for.
    :return: A set of synonyms for the word.
    """

    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms


# Load the emoji-keyword mapping
emoji_keywords_df = pd.read_csv("emoji_book_rec/data/emoji_keyword_list.tsv", sep="\t")
keywords = set()
for _, row in emoji_keywords_df.iterrows():
    for kw in row[1:]:
        keywords.add(kw.lower())
keywords = sorted(keywords)

# Load the books data
books_df = pd.read_csv("emoji_book_rec/data/BooksDatasetClean.csv")
books_df = books_df[books_df["Description"].notna() & (books_df["Description"].str.strip() != "")]
books = (books_df["Title"] + " " + books_df["Authors"]).tolist()

# Initialize the 2D array
keyword_matrix = np.zeros((len(keywords), len(books)), dtype=float)

# Fill in the matrix
synonym_cache = {}

for i, kw in enumerate(keywords):
    if kw not in synonym_cache:
        synonym_cache[kw] = get_synonyms(kw) | {kw}  # include the keyword itself

    synonyms = synonym_cache[kw]

    for j, desc in enumerate(books_df["Description"].fillna("").str.lower()):
        count = sum(desc.count(syn) for syn in synonyms)
        if desc:
            keyword_matrix[i, j] = float(count) / len(desc) * 100
        else:
            keyword_matrix[i, j] = count

# Convert to DataFrame for easy inspection or export
result_df = pd.DataFrame(keyword_matrix, index=keywords, columns=books)

# Save to file
result_df.to_csv("emoji_book_rec/data/keyword_book_matrix.tsv", sep="\t")
