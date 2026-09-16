from model.Article import Article
from mail.email_generator import generate_email

def test_generate_email():
    article = Article(
        title="Test Article",
        summary="This is a test article.",
        category="Technology",
        importance="High",
        url="https://example.com/test-article"
    )
    articles = [article]
    contenu_html = generate_email(articles)
    assert "Test Article" in contenu_html
    assert "This is a test article." in contenu_html

    print("Test passed: Email content generated successfully.")
    print(contenu_html)  # Affiche le contenu HTML généré pour vérification