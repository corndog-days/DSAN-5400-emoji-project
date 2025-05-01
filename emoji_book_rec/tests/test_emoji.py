import pytest
import pandas as pd

@pytest.fixture
def keyword_matrix():
    return pd.read_csv("emoji_book_rec/data/keyword_book_matrix.tsv", sep="\t", index_col=0)

@pytest.fixture
def emoji_keywords():
    emoji_dict = {}
    with open("emoji_book_rec/data/emoji_keyword_list.tsv", encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if parts:
                emoji_dict[parts[0]] = parts[1:]
    return emoji_dict

@pytest.fixture
def raw_books():
    books_df = pd.read_csv("emoji_book_rec/data/BooksDatasetClean.csv")
    books_df = books_df[books_df["Description"].notna() & (books_df["Description"].str.strip() != "")]
    return books_df

def test_keywords_in_matrix(emoji_keywords, keyword_matrix):
    all_keywords = {kw.strip().lower() for kws in emoji_keywords.values() for kw in kws}
    matrix_keywords = {kw.strip().lower() for kw in keyword_matrix.index}
    missing_keywords = all_keywords - matrix_keywords
    assert not missing_keywords, f"Missing keywords in matrix: {missing_keywords}"

def test_books_in_matrix(keyword_matrix, raw_books):
    matrix_books = set(keyword_matrix.columns)
    book_titles_authors = {
        f"{row['Title']} {row['Authors']}" for _, row in raw_books.iterrows()
    }
    missing_books = book_titles_authors - matrix_books
    if missing_books:
        print("\nSample missing book titles/authors:")
        for book in list(missing_books)[:10]:
            print(f"  - {book}")
    assert not missing_books, f"{len(missing_books)} books missing from matrix"