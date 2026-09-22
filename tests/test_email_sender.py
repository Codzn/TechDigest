from model.Article import Article
from mail.email_generator import generate_email
from mail.email_sender import envoyer_veille_technologique

article1 = Article(
    title="Test Article",
    summary="This is a test article.",
    category="Technology",
    importance="High",
    url="https://example.com/test-article"
)

article2 = Article(
    title="Another Test Article",
    summary="This is another test article.",
    category="Science",
    importance="Medium",
    url="https://example.com/another-test-article"
)

article3 = Article(
    title="Third Test Article",
    summary="This is the third test article.",
    category="Health",
    importance="Low",
    url="https://example.com/third-test-article"
)

articles = [article1, article2, article3]

contenu_html = generate_email(articles)

envoyer_veille_technologique(contenu_html)