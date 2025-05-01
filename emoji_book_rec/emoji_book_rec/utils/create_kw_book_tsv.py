"""Create a keyword-book matrix from the emoji-keyword mapping and book descriptions.
This script generates a matrix where each row corresponds to a keyword (or its synonyms)"""

import pandas as pd
import numpy as np
from nltk.corpus import wordnet
import argparse
import gdown
import zipfile

parser = argparse.ArgumentParser(description="Create keyword-book matrix")
parser.add_argument("-f", "--filepath", required=False, help="Path to user dataset", default=None)
args = parser.parse_args()

# download and unzip dataset if not already in data folder
if args.filepath is None:
    url = "https://drive.google.com/uc?id=1Ai0rmMPnyJHcP1bTdFm0T89-UMJ3uOK_"
    zip_path = "data.zip"
    extract_dir = "emoji_book_rec/data"

    if not os.path.exists(zip_path):
        gdown.download(url, zip_path, quiet=False)

    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

    args.filepath = os.path.join(extract_dir, "BooksDatasetClean.csv")


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
books_df = pd.read_csv(args.filepath)
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
