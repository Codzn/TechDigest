from filtrage import filter_news
from news_collector import get_news





if __name__ == "__main__":
    data = get_news()
    filtered_data = filter_news(data)
    print(filtered_data)