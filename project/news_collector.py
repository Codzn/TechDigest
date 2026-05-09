from dotenv import load_dotenv
import os
import requests

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API")

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching news: {e}")
        return {"articles": []}

data = get_news()

print(data)

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


