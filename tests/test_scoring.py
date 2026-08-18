import json
from filters.filtrage import filter_news, articles_sorted_by_score

with open("data/test_articles.json", "r") as f:
    test_news_data = json.load(f)

filtered_articles = filter_news(test_news_data)
sorted_articles = articles_sorted_by_score(filtered_articles)

print(sorted_articles)


