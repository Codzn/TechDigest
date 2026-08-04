from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API")

def get_news():
    """
    Récupère les acutalités depuis NewsApi.

    Retour : 
        dict : Un dictionnaire contenant les articles d'actualités.
    """
    try:
        date_hier = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        keywords = (
            '"système d\'information" OR "systèmes d\'information" OR ERP OR SAP OR CRM OR PLM OR '
            '"transformation numérique" OR "transformation digitale" OR "industrie 4.0" OR "jumeau numérique" OR '
            '"cybersécurité" OR "intelligence artificielle" OR "cloud" OR "data analytics" OR "supply chain" OR '
            'MES OR "digital twin"'
        )
        url = f"https://newsapi.org/v2/everything?q={keywords}&language=fr&sortBy=publishedAt&from={date_hier}&pageSize=100&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching news: {e}")
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
        print(f"Error printing news: {e}")


