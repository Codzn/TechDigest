from dotenv import load_dotenv
import os
import requests

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API")

url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"

response = requests.get(url)
data = response.json()

articles = data["articles"]

for article in articles:
    print(f"Title: {article['title']}")
    print(f"Description: {article['description']}")
    print(f"URL: {article['url']}")
    print("-" * 80)

