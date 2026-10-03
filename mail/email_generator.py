def generate_email(articles):
    """
    Generates the email content from the summarized articles.
    """
    contenu_html = """
    <p>Hello,</p>
    <p>Here are the summaries of the latest technology articles:</p>
    """
    
    for article in articles:
        contenu_html += f"<h2><strong>Titre:</strong> {article.title}</h2>"
        contenu_html += f"<p><strong>Résumé:</strong> {article.summary}</p>"
        contenu_html += f"<p><strong>Catégorie:</strong> {article.category}</p>"
        contenu_html += f"<p><strong>Importance:</strong> {article.importance}</p>"
        contenu_html += f"<p><strong>URL:</strong> <a href='{article.url}'>{article.url}</a></p>"
    
    contenu_html += "<p>Sincerely,<br/>The Team TechDigest</p>"
    
    return contenu_html
