""" Edit:  we are no longer using API's for data
This class will save API query search data into a large dataset TSV file"""

import dataclasses
import pandas as pd
import requests
from typing import List


@dataclasses.dataclass
class Results:
    """class stores API search results in a dataclass object"""

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


class BookAPI:
    """Class to fetch book data from various APIs and save it to a TSV file."""

    def __init__(self):
        """Initialize the API URLs."""
        self.google_books_url = "https://www.googleapis.com/books/v1/volumes"
        self.open_library_url = "https://openlibrary.org/search.json"
        self.iarchive_url = "https://archive.org/advancedsearch.php"

    def google_books_api(self, query: str) -> List[Results]:
        """Fetch data from Google Books API.
        :param query: Search query string.
        :return: List of book results."""
        params = {"q": query}
        response = requests.get(self.google_books_url, params=params)
        if not response.text.strip():
            print(f"Empty response for query '{query}'. Skipping.")
            return []
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON for query '{query}': {e}")
            return []

        books = []
        if "items" in data:
            for item in data["items"]:
                volume_info = item.get("volumeInfo", {})
                books.append(
                    Results(
                        title=volume_info.get("title"),
                        authors=", ".join(volume_info.get("authors", [])),
                        publisher=volume_info.get("publisher"),
                        publishedDate=volume_info.get("publishedDate"),
                        description=volume_info.get("description"),
                        pageCount=volume_info.get("pageCount"),
                        categories=(
                            ", ".join(volume_info.get("categories", [])) if volume_info.get("categories") else None
                        ),
                        averageRating=volume_info.get("averageRating"),
                        ratingsCount=volume_info.get("ratingsCount"),
                        language=volume_info.get("language"),
                    )
                )

        return books

    def open_library_api(self, query: str) -> List[Results]:
        """Fetch data from Open Library API.
        :param query: Search query string.
        :return: List of book results."""
        params = {"q": query}
        response = requests.get(self.open_library_url, params=params)

        if not response.text.strip():
            print(f"Empty response for query '{query}'. Skipping.")
            return []
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON for query '{query}': {e}")
            return []

        books = []
        if "docs" in data:
            for item in data["docs"]:
                books.append(
                    Results(  # Open Library does not provide all fields saved as "None"
                        title=item.get("title"),
                        authors=", ".join(item.get("author_name", [])),
                        publisher=None,
                        publishedDate=item.get("first_publish_year"),
                        description=None,
                        pageCount=None,
                        categories=None,
                        averageRating=None,
                        ratingsCount=None,
                        language=", ".join(item.get("language", [])),
                    )
                )
        return books

    def iarchive_api(self, query):
        """Fetch data from Internet Archive API using a search query.
        :param query: Search query string.
        :return: List of book results."""
        params = {
            "q": f'title:("{query}")',
            "fl[]": ["title", "creator", "language", "publisher", "description", "date"],
            "output": "json",
        }
        response = requests.get(self.iarchive_url, params=params)
        if not response.text.strip():
            print(f"Empty response for query '{query}'. Skipping.")
            return []
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON for query '{query}': {e}")
            return []

        # print(data)
        books = []

        if "response" in data and "docs" in data["response"]:
            for item in data["response"]["docs"]:
                books.append(
                    Results(
                        title=item.get("title", ""),
                        authors=(
                            ", ".join(item.get("creator", []))
                            if isinstance(item.get("creator"), list)
                            else item.get("creator", "")
                        ),
                        publisher=item.get("publisher", ""),
                        publishedDate=item.get("date", ""),
                        description=item.get("description", ""),
                        pageCount=None,
                        categories=None,
                        averageRating=None,
                        ratingsCount=None,
                        language=(
                            ", ".join(item.get("language", []))
                            if isinstance(item.get("language"), list)
                            else item.get("language", "")
                        ),
                    )
                )
        return books

    def get_combined_data(self, query: str) -> pd.DataFrame:
        """Combine data from both APIs into a single pandas DataFrame.
        :param query: Search query string.
        :return: DataFrame containing combined book data."""

        google_books = self.google_books_api(query)
        open_library_books = self.open_library_api(query)
        iarchive_books = self.iarchive_api(query)

        all_books = google_books + open_library_books + iarchive_books

        df = pd.DataFrame([book.to_dict() for book in all_books])
        df.drop_duplicates(subset="title", keep="first", inplace=True)
        # print(df["title"])
        return df

    def save_to_tsv(self, query: str, filename="books_data.tsv"):
        """Fetch and save combined book data to a TSV file.
        :param query: Search query string.
        :param filename: Name of the output TSV file.
        :return: None"""
        df = self.get_combined_data(query)
        df.to_csv(filename, sep="\t", index=False)
        print(f"Saved {len(df)} records to {filename}")


# if __name__ == "__main__":
#     user_query = input("Enter your book search query: ")
#     book_api = BookAPI()
#     book_api.save_to_tsv(user_query, "combined_books_data.tsv")
