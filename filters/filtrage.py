from collectors.news_collector import get_news
import re

SI_KEYWORDS = ["artificial intelligence", "machine learning", "deep learning", "neural networks", "natural language processing", "computer vision", "robotics", "automation", "data science", "big data", "cloud computing", "edge computing", "quantum computing", "cybersecurity", "ethics in ai", "ai in healthcare", "ai in finance", "ai in education", "ai in transportation", "plm", "erp", "crm", "supply chain management", "manufacturing execution systems", "mes", "digital twin", "industry 4.0", "smart factory", "iot in manufacturing", "predictive maintenance", "ai in manufacturing"]


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

def calculate_score(article):
    score = 0
    for keyword in SI_KEYWORDS:
        if keyword in article["title"]:
            score += 2  # Plus de poids pour les mots-clés dans le titre
        if keyword in article["description"]:
            score += 1  # Moins de poids pour les mots-clés dans la description

    return score

def filter_news(data):
    """
    Récupère les articles renvoyés par l'API.

    Retour : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    """
    filtered_news = []
    try:
        articles = data["articles"]
        for article in articles:
            article["title"] = clean_text(article["title"])
            article["description"] = clean_text(article["description"])
            if article["title"] == "" or article["description"] == "":
                continue
            score = calculate_score(article)
            if score > 0:
                filtered_news.append(article)
                print(article["title"])
                print(score)
                print("----------------")   
    except KeyError:
        print("Error: Invalid data format")
    return filtered_news

print("Filtrage des actualités en cours...")
filtered_news = filter_news(get_news())