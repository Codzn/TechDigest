from model.Article import Article
from unittest.mock import patch, Mock
from ia.summarizer import summarize_article

def test_summarize_article():
    # Créez un article de test
    article = Article(
        title="L'IA dans les entreprises",
        url="https://example.com/article",
        description="Une entreprise adopte une nouvelle solution d'IA."
    )

    fake_response = Mock()
    fake_response.text = (
        '{"summary": "Une entreprise adopte une solution d\'IA.",'
        '"category": "Intelligence artificielle",'
        '"importance": "Élevée"}'
    )

    # Patch the requests.get method to return the fake response
    with patch("ia.summarizer.genai.Client") as mock_client:

        fake_client = mock_client.return_value
        fake_client.models.generate_content.return_value = fake_response

        result = summarize_article([article])

        # Assert the expected values
    assert len(result) == 1
    assert result[0] is article
    assert article.summary == "Une entreprise adopte une solution d'IA."
    assert article.category == "Intelligence artificielle"
    assert article.importance == "Élevée"
    assert (
    mock_client.return_value.models.generate_content.return_value
    is fake_response
)

    mock_client.return_value.models.generate_content.assert_called_once()
