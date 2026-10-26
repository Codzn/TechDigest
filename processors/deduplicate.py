from .filtrage import clean_text

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

def remove_duplicates(filtered_news):
    """
    Remove duplicate articles based on Jaccard similarity of titles.
    Jaccard similarity is a measure of similarity between two sets, defined as the size of the intersection divided by the size of the union of the sets.
    If the Jaccard similarity between two titles is above a certain threshold (e.g., 0.8), they are considered duplicates.
    """
    unique_articles = []
    for article1 in filtered_news:
        matching_indx = None
        for indx, article2 in enumerate(unique_articles): # Compare each article with the articles already in unique_articles
            if jaccard_similarity(article1.title, article2.title) > 0.5:  # Adjust threshold as needed
                matching_indx = indx
        if matching_indx is None:
            unique_articles.append(article1)
        else:
            if article1.score > unique_articles[matching_indx].score:
                unique_articles[matching_indx] = article1  # Replace with the article with the higher score
    return unique_articles
