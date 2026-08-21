from .filtrage import clean_text

import re

def normalize_title(title):
    """
    Normalize the title by converting it to lowercase and stripping whitespace.
    """
    cleaned_title = clean_text(title)
    return cleaned_title


def get_words(title):
    """
    Split the title into words and return a set of unique words.
    """
    normalized_title = normalize_title(title)
    words = set(normalized_title.split())
    return words

def jaccard_similarity(title1, title2):
    """
    Calculate the Jaccard similarity between two titles.
    """
    words1 = get_words(title1)
    words2 = get_words(title2)
    intersection = len(words1.intersection(words2)) # Taille de la liste des mots communs entre les deux titres
    union = len(words1.union(words2)) # Taille de la liste des mots uniques entre les deux titres
    return intersection / union if union != 0 else 0

def remove_duplicates(articles):
    """
    Remove duplicate articles based on Jaccard similarity of titles.
    Jaccard similarity is a measure of similarity between two sets, defined as the size of the intersection divided by the size of the union of the sets.
    If the Jaccard similarity between two titles is above a certain threshold (e.g., 0.8), they are considered duplicates.
    """
    unique_articles = []
    for i, article1 in enumerate(articles):
        is_duplicate = False
        for j, article2 in enumerate(articles[:i]): # Compare the current article with all previous articles before i ? 
            if jaccard_similarity(article1['title'], article2['title']) > 0.8:  # Adjust threshold as needed
                is_duplicate = True
                break
        if not is_duplicate:
            unique_articles.append(article1)
    return unique_articles
