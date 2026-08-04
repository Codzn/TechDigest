SI_KEYWORDS = ["AI", "Artificial Intelligence", "Machine Learning", "Deep Learning", "Neural Networks", "Natural Language Processing", "Computer Vision", "Robotics", "Automation", "Data Science", "Big Data", "Cloud Computing", "Edge Computing", "Quantum Computing", "Cybersecurity", "Ethics in AI", "AI in Healthcare", "AI in Finance", "AI in Education", "AI in Transportation", "PLM", "ERP", "CRM", "Supply Chain Management", "Manufacturing Execution Systems", "MES", "Digital Twin", "Industry 4.0", "Smart Factory", "IoT in Manufacturing", "Predictive Maintenance", "AI in Manufacturing"]

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
