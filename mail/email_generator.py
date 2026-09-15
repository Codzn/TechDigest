def generate_email(articles):
    """
    Génère le contenu de l'e-mail à partir des articles résumés.
    """
    contenu_html = """
    <p>Bonjour,</p>
    <p>Voici les résumés des articles de la veille technologique :</p>
    """
    
    for article in articles:
        contenu_html += f"<h2><strong>Titre:</strong> {article.title}</h2>"
        contenu_html += f"<p><strong>Résumé:</strong> {article.summary}</p>"
        contenu_html += f"<p><strong>Catégorie:</strong> {article.category}</p>"
        contenu_html += f"<p><strong>Importance:</strong> {article.importance}</p>"
        contenu_html += f"<p><strong>URL:</strong> <a href='{article.url}'>{article.url}</a></p>"
    
    contenu_html += "<p>Cordialement,<br/>L'équipe TechDigest</p>"
    
    return contenu_html
