from model.Article import Article
from unittest.mock import patch, Mock
from ia.summarizer import summarize_article

def test_summarize_article(monkeypatch):

    monkeypatch.setenv("CLE_GEMINI", "fake_api_key")

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

def test_summarize_article_continue_after_failure(monkeypatch):

    monkeypatch.setenv("CLE_GEMINI", "fake_api_key")

    article_failed = Article(
        title="Article en échec",
        url="https://example.com/failed"
    )
   
   
    # Créez un article de test
    article_success = Article(
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
    with patch("ia.summarizer.genai.Client") as mock_client,\
    patch("ia.summarizer.time.sleep"):
        
        generate_content = (
            mock_client.return_value.models.generate_content
        )

        generate_content.side_effect = [
            Exception("Erreur serveur 503"),
            Exception("Erreur serveur 503"),
            Exception("Erreur serveur 503"),
            fake_response
            ]
        result = summarize_article([article_failed, article_success])

        assert len(result) == 1
        assert result[0] is article_success
        assert article_success.summary == "Une entreprise adopte une solution d'IA."
        assert article_success.category == "Intelligence artificielle"
        assert article_failed.summary is None
        assert generate_content.call_count == 4

def test_summarize_article_stops_on_quota_exceeded(monkeypatch):

    monkeypatch.setenv("CLE_GEMINI", "fake-api-key")

    article_success = Article(
        title="Article réussi",
        url="https://example.com/success"
    )
    article_blocked = Article(
        title="Article bloqué",
        url="https://example.com/blocked"
    )

    fake_response = Mock()
    fake_response.text = (
        '{"summary": "Résumé valide", '
        '"category": "IA", '
        '"importance": "Élevée"}'
    )

    with patch("ia.summarizer.genai.Client") as mock_client:
        generate_content = (
            mock_client.return_value.models.generate_content
        )

        generate_content.side_effect = [
            fake_response,
            Exception("429 RESOURCE_EXHAUSTED")
        ]

        result = summarize_article([article_success, article_blocked])

    assert len(result) == 1
    assert result[0] is article_success
    assert article_success.summary == "Résumé valide"
    assert article_blocked.summary is None
    assert generate_content.call_count == 2
