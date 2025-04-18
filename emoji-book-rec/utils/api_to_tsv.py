import dataclasses
import pandas as pd
import requests
from typing import List

@dataclasses.dataclass
class Book:
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
    def __init__(self):
        self.google_books_url = "https://www.googleapis.com/books/v1/volumes"
        self.open_library_url = "https://openlibrary.org/search.json"

    def google_books_api(self, query: str) -> List[Book]:
        """Fetch data from Google Books API."""
        params = {"q": query, "maxResults": 1}
        response = requests.get(self.google_books_url, params = params)
        data = response.json()

        books = []
        if "items" in data:
            for item in data["items"]:
                volume_info = item.get("volumeInfo", {})
                books.append(Book(
                    title=volume_info.get("title"),
                    authors=", ".join(volume_info.get("authors", [])),
                    publisher=volume_info.get("publisher"),
                    publishedDate=volume_info.get("publishedDate"),
                    description=volume_info.get("description"),
                    pageCount=volume_info.get("pageCount"),
                    categories=", ".join(volume_info.get("categories", [])) if volume_info.get("categories") else None,
                    averageRating=volume_info.get("averageRating"),
                    ratingsCount=volume_info.get("ratingsCount"),
                    language=volume_info.get("language")
                ))

        return books

    def open_library_api(self, query: str) -> List[Book]:
        """Fetch data from Open Library API."""
        params = {"q": query}
        response = requests.get(self.open_library_url, params=params)
        data = response.json()

        books = []
        if "docs" in data:
            for item in data["docs"]:
                books.append(Book( # Open Library does not provide all fields saved as "None"
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
                ))
        return books

    def get_combined_data(self, query: str) -> pd.DataFrame:
        """Combine data from both APIs into a single pandas DataFrame."""

        google_books = self.google_books_api(query)
        open_library_books = self.open_library_api(query)

        all_books = google_books + open_library_books

        df = pd.DataFrame([book.to_dict() for book in all_books])
        df.drop_duplicates(subset='title', keep='first', inplace=True)
        print(df["title"])
        return df

    def save_to_tsv(self, query: str, filename="books_data.tsv"):
        """Fetch and save combined book data to a TSV file."""
        df = self.get_combined_data(query)
        df.to_csv(filename, sep='\t', index=False)
        print(f"Saved {len(df)} records to {filename}")

