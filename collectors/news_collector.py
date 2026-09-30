from dotenv import load_dotenv
import os
import requests
import datetime
import logging


load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API")

def get_news():
    """
    Récupère les acutalités depuis NewsApi.

    Retour : 
        dict : Un dictionnaire contenant les articles d'actualités.
    """
    try:
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
        keywords = (
            '"système d\'information" OR "systèmes d\'information" OR ERP OR SAP OR CRM OR PLM OR '
            '"transformation numérique" OR "transformation digitale" OR "industrie 4.0" OR "jumeau numérique" OR '
            '"cybersécurité" OR "intelligence artificielle" OR "cloud" OR "data analytics" OR "supply chain" OR '
            'MES OR "digital twin"'
        )

        params = {
            "q": keywords,
            "language": "fr",
            "sortBy": "publishedAt",
            "from": last_week,
            "to": datetime.date.today().isoformat(),
            "pageSize": 100,
            "apiKey": NEWS_API_KEY
        }
        response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return {"articles": []}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"articles": []}


def print_news(data):
    try:
        articles = data["articles"]
        for article in articles: 
                print(f"Title: {article['title']}")
                print(f"Description: {article['description']}")
                print(f"URL: {article['url']}")
                print("-" * 80)
    except Exception as e:
        logging.error(f"Error printing news: {e}")

"""
Retourne bien le titre et la description de chaque article, ainsi que l'URL de l'article.
"""

"""
print("Récupération des actualités en cours...")
news_data = get_news()
print_news(news_data)
"""

