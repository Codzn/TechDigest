from collectors.news_collector import get_news
import re

SI_KEYWORDS = {"artificial intelligence" : 2, "machine learning" : 2, "deep learning" : 2, "neural networks" : 2, "natural language processing" : 2, "computer vision" : 2, "robotics" : 1, "automation" : 2, "data science" : 2, "big data" : 2, "cloud computing" : 2, "edge computing" : 2, "quantum computing" : 2, "cybersecurity" : 2,  "ai in finance" : 2, "plm" : 3, "erp" : 3, "crm" : 3, "supply chain management" : 1, "manufacturing execution systems" : 1, "mes" : 1, "digital twin" : 1, "industry 4.0" : 1, "smart factory" : 1, "iot in manufacturing" : 1, "predictive maintenance" : 1, "SAP" : 3, "microsoft dynamics" : 3, "oracle" : 3, "salesforce" : 3, "siemens" : 3, "autodesk" : 3, "pdm" : 3, "cad" : 3, "cam" : 3, "plm software" : 3, "erp software" : 3, "crm software" : 3, "dassault systemes" : 3, "industrial IoT": 1, "vulnerabiility": 1}

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
    bonus_points = 3
    occurence = 0
    for keyword, points in SI_KEYWORDS.items():
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        if re.search(pattern, title):
            score += points * 2 # Les mots-clés dans le titre ont un poids double
            occurence += 1
            if occurence > 2:
                score += bonus_points # Bonus si plus de 2 mots-clés sont trouvés dans le titre
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
            if score > 5:   # Seuil de score pour inclure l'article dans les résultats filtrés
                filtered_news[article["url"]] = {
                    "title": title,
                    "description": description,
                    "score": score
                }
                """
                print("Title:", title)
                print("Description:", description)
                print("URL:", article.get("url", "N/A"))
                print("Score:", score)
                print("----------------")   
                """
    except KeyError:
        print("Error: Invalid data format")
    return filtered_news


def articles_sorted_by_score(filtered_news):
    """
    Récupère : Un dictionnaire d'articles filtrés.
    Retour : Une liste d'articles triés par score décroissant.
    """
    return sorted(filtered_news.items(), key=lambda x: (x[1].get("score") or 0), reverse=True)



"""
print("Filtrage des actualités en cours...")
filtered_articles = filter_news(get_news())
sorted_articles = articles_sorted_by_score(filtered_articles)
print(f"Nombre d'articles filtrés : {len(sorted_articles)}")
"""