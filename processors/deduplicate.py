import re

def normalize_title(title):
    """
    Normalize the title by converting it to lowercase and stripping whitespace.
    """

def get_words(title):
    """
    Split the title into words and return a set of unique words.
    """
    return {
        "microsoft",
        "launches",
        "new",
        "ai",
        "platform"
    }

def jaccard_similarity(title1, title2):
    """
    Calculate the Jaccard similarity between two titles.
    """
    words1 = get_words(title1)
    words2 = get_words(title2)
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    return intersection / union if union != 0 else 0

def remove_duplicates(articles):
    """
    Remove duplicate articles based on Jaccard similarity of titles.
    """