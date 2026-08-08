from collectors.news_collector import get_news

SI_KEYWORDS = ["artificial intelligence", "machine learning", "deep learning", "neural networks", "natural language processing", "computer vision", "robotics", "automation", "data science", "big data", "cloud computing", "edge computing", "quantum computing", "cybersecurity", "ethics in ai", "ai in healthcare", "ai in finance", "ai in education", "ai in transportation", "plm", "erp", "crm", "supply chain management", "manufacturing execution systems", "mes", "digital twin", "industry 4.0", "smart factory", "iot in manufacturing", "predictive maintenance", "ai in manufacturing"]


def clean_text(text):
    """
    Récupère : Un texte brut.
    Retour : Le texte nettoyé en supprimant les caractères spéciaux et les espaces inutiles.
    """
    if text is None:
        return ""
    # Supprimer les caractères spéciaux et les espaces inutiles
    cleaned_text = text.replace("\n", " ").replace("\r", " ").strip()
    return cleaned_text

def filter_news(data):
    """
    Récupère les articles renvoyés par l'API.

    Retour : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    """
    filtered_news = []
    try:
        articles = data["articles"]
        for article in articles:
            if article["title"] is None or article["description"] is None:
                continue
            if any(keyword in article["title"] for keyword in SI_KEYWORDS) or any(keyword in article["description"] for keyword in SI_KEYWORDS):
                filtered_news.append(article)
    except KeyError:
        print("Error: Invalid data format")
    return filtered_news

print(filter_news(get_news()))
