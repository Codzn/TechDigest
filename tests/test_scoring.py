import json
from filters.filtrage import filter_news, articles_sorted_by_score

with open("tests/test_news.json", "r") as f:
    test_news_data = json.load(f)
