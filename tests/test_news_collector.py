from collectors.news_collector import get_news
import json

from unittest.mock import patch, MagicMock, Mock

@patch('collectors.news_collector.requests.get')
def test_get_news(mock_get):
    mock_get.side_effect = Exception("API request failed")

    result = get_news()
    assert result == {"articles": []}

@patch('collectors.news_collector.requests.get')
def test_get_news_success(mock_get):
    mock_response = Mock()

    fake_data = {
    "articles": [
        {
            "title": "...",
            "description": "...",
            "url": "..."
        }
    ]
}
    mock_response.json.return_value = fake_data
    mock_response.raise_for_status.return_value = None
   
    mock_get.return_value = mock_response

    result = mock_response

    assert result == fake_data

