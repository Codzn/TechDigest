from collectors.news_collector import get_news
import requests
import pytest

from unittest.mock import patch, MagicMock, Mock

@patch('collectors.news_collector.requests.get')
def test_get_news_request_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Connection failed"
    )
    with pytest.raises(RuntimeError, match="NewsAPI request failed"):
        get_news()

    mock_get.assert_called_once()



@patch('collectors.news_collector.requests.get')
def test_get_news_unexpected_error(mock_get):
    mock_get.side_effect = TypeError("Unexpected failure")

    with pytest.raises(RuntimeError, match="Unexpected error while fetching news"):
        get_news() # type: ignore

    mock_get.assert_called_once()


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

    result = mock_response.json()

    assert result == fake_data

