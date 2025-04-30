import pandas as pd
import emoji
from api_to_tsv import BookAPI
import csv


def load_emoji_keyword_dict(path="emoji_book_rec/data/emoji_keyword_list.tsv"):
    """
    Loads emoji-keyword mappings from a TSV file.
    :return: Dict[str, List[str]]
    """
    df = pd.read_csv(path, sep="\t")
    emoji_kw_dict = {}

    for index, row in df.iterrows():
        # Remove leading spaces if they exist
        emoji_name = row["Emoji"].strip()
        # Convert emoji name to emoji
        unicode_emoji = emoji.emojize(f":{emoji_name}:", language="alias")
        keywords = [kw.strip() for kw in row[1:].dropna()]
        emoji_kw_dict[unicode_emoji] = keywords

    return emoji_kw_dict


def populate_dataset(
    emoji_kw_tsv_path="emoji_book_rec/data/emoji_keyword_list.tsv", output_path="emoji_book_rec/data/books_data.tsv"
):
    emoji_kw_dict = load_emoji_keyword_dict(emoji_kw_tsv_path)
    book_api = BookAPI()

    all_keywords = set()
    for kws in emoji_kw_dict.values():
        all_keywords.update(kws)

    print(f"Total unique keywords to query: {len(all_keywords)}")

    combined_df = pd.DataFrame()

    for i, keyword in enumerate(sorted(all_keywords)):
        print(f"[{i+1}/{len(all_keywords)}] Fetching data for keyword: {keyword}")
        new_df = book_api.get_combined_data(keyword)

        # Append and deduplicate
        combined_df = pd.concat([combined_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset="title", keep="first", inplace=True)

    combined_df.to_csv(output_path, sep="\t", index=False)
    print(f"\n Saved final dataset with {len(combined_df)} unique books to {output_path}")


if __name__ == "__main__":
    populate_dataset()
