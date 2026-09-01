import json
from processors.filtrage import filter_news, articles_sorted_by_score
from processors.deduplicate import remove_duplicates
from ia.summarizer import summarize_article

with open("data/test_articles.json", "r") as f:
    test_news_data = json.load(f)

filtered_articles = filter_news(test_news_data)
unique_articles = remove_duplicates(filtered_articles)
sorted_articles = articles_sorted_by_score(unique_articles)
summary = summarize_article(sorted_articles)