import json
from processors.filtrage import filter_news, articles_sorted_by_score

with open("data/test_articles.json", "r") as f:
    test_news_data = json.load(f)

filtered_articles = filter_news(test_news_data)
sorted_articles = articles_sorted_by_score(filtered_articles)
print("Nombre d'articles filtrés :", len(sorted_articles))
print("\n")
print("Articles filtrés et triés par score décroissant :")
print("\n")
for url, article in sorted_articles:
    print(f"URL: {url}")
    print(f"Title: {article['title']}")
    print(f"Description: {article['description']}")
    print(f"Score: {article['score']}")
    print("-" * 80)

