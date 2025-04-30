"""Edit:  we are no longer using API's for data
Parse TSV files and convert them to Book objects."""

import abc
import csv
import collections.abc
import dataclasses
from .api_to_tsv import Book
from typing import Dict, List, Tuple


@dataclasses.dataclass
class Book:
    """Class representing book information"""

    title: str
    authors: str = ""
    publisher: str = ""
    publishedDate: str = ""
    description: str = ""
    pageCount: int = 0
    categories: str = ""
    averageRating: float = None
    ratingsCount: int = None
    language: str = ""

    def to_dict(self):
        return dataclasses.asdict(self)


class DocIterator(abc.ABC, collections.abc.Iterator):
    """Abstract base class for document iterators"""

    def __str__(self):
        return self.__class__.__name__


class TsvIterator(DocIterator):
    """Iterator to iterate over tsv-formatted documents"""

    def __init__(self, path):
        """
        Args:
            path (str): Path to the TSV file.
        """
        self.path = path
        self.fp = open(self.path)
        self.reader = csv.reader(self.fp, delimiter="\t")
        next(self.reader)  # skip first row

    def __iter__(self):
        """Return self as an iterator."""
        return self

    def __next__(self):
        """Return the next book object from the TSV file."""
        try:
            row = next(self.reader)
            # print(Comparison(row[0], row[1], row[2]))
            # true_label = float(row[2])
            return Book(
                title=row.get("title", ""),
                authors=row.get("authors", ""),
                publisher=row.get("publisher", ""),
                publishedDate=row.get("publishedDate", ""),
                description=row.get("description", ""),
                pageCount=int(row.get("pageCount", 0)) if row.get("pageCount") else 0,
                categories=row.get("categories", ""),
                averageRating=float(row.get("averageRating", 0)) if row.get("averageRating") else None,
                ratingsCount=int(row.get("ratingsCount", 0)) if row.get("ratingsCount") else None,
                language=row.get("language", ""),
            )
        except StopIteration:
            self.fp.close()
            raise


def get_top_books_from_scores(scores: List[Tuple[str, int]], books: List[Results], top_n: int = 5) -> List[Book]:
    """
    Given a sorted (title, score) list and original Results list, return top Book objects.
    :param scores: List of tuples (title, score) sorted by score.
    :param books: List of Results objects.
    :param top_n: Number of top books to return.
    :return: List of Book objects.
    """
    title_to_book = {book.title: book for book in books}
    selected_books = []

    for title, _ in scores[:top_n]:
        if title in title_to_book:
            book = title_to_book[title]
            selected_books.append(
                Book(
                    title=book.title,
                    authors=book.authors,
                    publisher=book.publisher,
                    publishedDate=book.publishedDate,
                    description=book.description,
                    pageCount=book.pageCount,
                    categories=book.categories,
                    averageRating=book.averageRating,
                    ratingsCount=book.ratingsCount,
                    language=book.language,
                )
            )

    return selected_books


def save_books_to_tsv(books: List[Book], filename: str = "selected_sorted_books.tsv"):
    """
    Save a list of Book objects to a TSV file.
    :param books: List of Book objects to save.
    :param filename: Name of the output TSV file.
    :return: None
    """
    if not books:
        print("No books to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        headers = books[0].__dataclass_fields__.keys()
        writer.writerow(headers)

        for book in books:
            writer.writerow([getattr(book, field) for field in headers])

    print(f"Top books saved to {filename}")
