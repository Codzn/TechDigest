from collectors.news_collector import get_news
import re

SI_KEYWORDS = {"artificial intelligence" : 2, "machine learning" : 2, "deep learning" : 2, "neural networks" : 2, "natural language processing" : 2, "computer vision" : 2, "robotics" : 1, "automation" : 2, "data science" : 2, "big data" : 2, "cloud computing" : 2, "edge computing" : 2, "quantum computing" : 2, "cybersecurity" : 2,  "ai in finance" : 2, "plm" : 3, "erp" : 3, "crm" : 3, "supply chain management" : 1, "manufacturing execution systems" : 1, "mes" : 1, "digital twin" : 1, "industry 4.0" : 1, "smart factory" : 1, "iot in manufacturing" : 1, "predictive maintenance" : 1}

def clean_text(text):
    """
    Récupère : Un texte brut.
    Retour : Le texte nettoyé en supprimant les caractères spéciaux et les espaces inutiles.
    """
    if text is None:
        return ""
    # Supprimer les caractères spéciaux et les espaces inutiles
    cleaned_text = re.sub(r'[\n\r\-]+', ' ', text)
    cleaned_final = cleaned_text.lower().strip()
    return cleaned_final

def calculate_score(title, description):
    score = 0
    for keyword, points in SI_KEYWORDS.items():
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        if re.search(pattern, title):
            score += points * 2  # Les mots-clés dans le titre ont un poids double
        if re.search(pattern, description):
            score += points

    return score

def filter_news(data):
    """
    Récupère les articles renvoyés par l'API.

    Retour : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    """
    filtered_news = {}
    try:
        articles = data["articles"]
        for article in articles:
            title = clean_text(article["title"])
            description = clean_text(article["description"])
            if not title or not description or not article.get("url"):
                continue
            score = calculate_score(title, description)
            if score > 2:
                 # Seuil de score pour inclure l'article dans les résultats filtrés
                filtered_news[article["url"]] = {
                    "title": title,
                    "description": description,
                    "score": score
                }
                print("Title:", title)
                print("Description:", description)
                print("URL:", article.get("url", "N/A"))
                print("Score:", score)
                print("----------------")   
    except KeyError:
        print("Error: Invalid data format")
    return filtered_news


def articles_sorted_by_score(filtered_news):
    """
    Récupère : Un dictionnaire d'articles filtrés.
    Retour : Une liste d'articles triés par score décroissant.
    """
    return sorted(filtered_news.items(), key=lambda x: x[1]["score"], reverse=True)

print("Filtrage des actualités en cours...")
filtered_articles = filter_news(get_news())
sorted_articles = articles_sorted_by_score(filtered_articles)
print(f"Nombre d'articles filtrés : {len(sorted_articles)}")