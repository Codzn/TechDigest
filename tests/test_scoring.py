import json
from processors.filtrage import filter_news, articles_sorted_by_score
from processors.deduplicate import remove_duplicates
from ia.summarizer import summarize_article

with open("data/test_articles.json", "r") as f:
    test_news_data = json.load(f)

filtered_articles = filter_news(test_news_data)
unique_articles = remove_duplicates(filtered_articles)
sorted_articles = articles_sorted_by_score(unique_articles)
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

summary = summarize_article(unique_articles)    