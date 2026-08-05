from collectors.news_collector import *
from filters.filtrage import *

if __name__ == "__main__":
    data = get_news()
    filtered_data = filter_news(data)
    print(filtered_data)