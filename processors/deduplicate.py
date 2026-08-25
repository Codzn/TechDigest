from .filtrage import clean_text, filter_news

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
        if not unique_articles: # If unique_articles is empty, add the first article
            unique_articles.append(article1) 
            break
        for article2 in unique_articles:
            if jaccard_similarity(article1['title'], article2['title']) > 0.8:  # Adjust threshold as needed
                score1 = article1['score']
                score2 = article2['score']
                if score1 > score2:
                    unique_articles.remove(article2)
                    unique_articles.append(article1)
                if score2 > score1:
                    break  # Keep the existing article with the higher score
                if score1 == score2:
                    # If scores are equal, keep the first one encountered (article2)
                    break
        else:
            unique_articles.append(article1)
    return unique_articles
