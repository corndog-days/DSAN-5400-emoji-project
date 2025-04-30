"""Create an inverted index of books based on keywords and their synonyms."""
from collections import defaultdict
from nltk.corpus import wordnet


def get_synonyms(word):
    """Get a set of synonyms for a word using WordNet.
    :param word: The word to find synonyms for.
    :return: A set of synonyms for the word."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms


def create_index(books, emoji_kw_dict):
    """
    Create inverted index of books per keyword or synonym found in description.
    :param books: List of Results objects
    :param emoji_kw_dict: Dict mapping emoji to keywords
    :return: Dict[keyword] = list of (title, count)
    """
    kw_book_index = defaultdict(list)

    # All keywords across all emojis
    all_keywords = set(kw for kws in emoji_kw_dict.values() for kw in kws)

    # Expand with synonyms
    expanded_keywords = {kw: {kw, *get_synonyms(kw)} for kw in all_keywords}

    for book in books:
        if not book.description:
            continue
        desc = book.description.lower()
        for kw, syns in expanded_keywords.items():
            count = sum(desc.count(syn) for syn in syns)
            if count > 0:
                kw_book_index[kw].append((book.title, count))

    return dict(kw_book_index)
