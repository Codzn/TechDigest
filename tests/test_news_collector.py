from collectors.news_collector import get_news

from unittest.mock import patch, MagicMock

@patch('collectors.news_collector.requests.get')
def test_get_news(mock_get):
    mock_get.side_effect = Exception("API request failed")

    result = get_news()
    assert result == {"articles": []}