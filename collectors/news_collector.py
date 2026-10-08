from dotenv import load_dotenv
import os
import requests
import datetime
import logging


load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API")

def get_news():
    """
    Retrieves news from NewsAPI.

    Returns:
        dict: A dictionary containing the news articles.
    """
    try:
        last_week = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
        keywords = ('"système d\'information" OR '
                    'ERP OR SAP OR CRM OR PLM OR '
                    '"transformation numérique" OR '
                    '"transformation digitale" OR '
                    '"industrie 4.0" OR '
                    '"jumeau numérique" OR '
                    'cybersécurité OR '
                    '"intelligence artificielle" OR '
                    'OpenAI OR ChatGPT OR '
                    '"machine learning" OR '
                    '"data science" OR '
                    '"cloud computing"'
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
        
        data = response.json() # means that the response is expected to be in JSON format and it will be converted into a Python dictionary.
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news: HTTP request failed")
        return {"articles": []}
    except Exception as e:
        logging.error(f"Unexpected error")
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


