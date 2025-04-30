"""This script reads a tab-separated values (TSV) file containing keywords
and their associated short texts, and converts it into a dictionary."""
# turns keyword tsv file from data folder into a dictionary and returns it


# used ChatGPT to help write parts of this function
def generate_keyword_dict(filepath):
    """
    Generate a dictionary from a TSV file containing keywords and their associated short texts.
    :param filepath: Path to the TSV file.
    :return: A dictionary where keys are short texts and values are lists of keywords.
    """
    # given a filepath as a string, create a dictionary
    # returns dict with shorttext as key, list of keywords as value
    keyword_dict = {}

    with open(filepath) as file:
        # skipping the header
        next(file)
        for line in file:
            parts = line.strip().split("\t")
            if parts:  # make sure the line is not empty
                shorttext = parts[0]
                keywords = parts[1:]

                # add extra weight to first keyword
                keywords.append(parts[1])
                keywords.append(parts[1])

                keyword_dict[shorttext] = keywords
    return keyword_dict
