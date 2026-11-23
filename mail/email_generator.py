from html import escape
from urllib.parse import urlparse

def generate_email(articles):

    """Generates a responsive and modern HTML email content from summarized articles."""
    
    if articles is None or len(articles) == 0:
        return "<html><body><p>Aucun article disponible.</p></body></html>"
    
    
    # HTML header and global styles
    contenu_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechDigest</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f6f9; padding: 20px 0;">
        <tr>
            <td align="center">
                <!-- Main Container -->
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #1a202c; padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0.5px;">TechDigest</h1>
                            <p style="color: #a0aec0; margin: 8px 0 0 0; font-size: 14px;">Votre veille tech de la semaine</p>
                        </td>
                    </tr>

                    <!-- Introduction -->
                    <tr>
                        <td style="padding: 30px 30px 10px 30px; color: #2d3748; font-size: 16px; line-height: 1.5;">
                            Bonjour,<br/><br/>
                            Voici une sélection des actualités tech de la semaine :
                        </td>
                    </tr>

                    <!-- Article List -->
                    <tr>
                        <td style="padding: 10px 30px 20px 30px;">
    """

    # Generate cards for each article
    for article in articles:
        # Dynamic badge color based on importance
        importance_bg = "#edf2f7"
        importance_color = "#4a5568"
        if str(article.importance).lower() in ["élevée", "elevée", "haute", "high", "3"]:
            importance_bg = "#feebc8"
            importance_color = "#c08021"

        summary= escape(article.summary) if article.summary else "Résumé indisponible."
        category = escape(article.category) if article.category else "Général"
        importance = escape(article.importance) if article.importance else "Non évaluée"
        title = escape(article.title) if article.title else "Sans titre"
        url = article.url or ""
        parsed_url = urlparse(url)
        if parsed_url.scheme in ["http", "https"] and parsed_url.netloc:
            url = escape(url, quote=True)
        else:
            url = ""

        contenu_html += f"""
                            <!-- Article Card -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 20px; border: 1px solid #e2e8f0; border-radius: 6px; background-color: #ffffff;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <!-- Metadata (Category & Importance) -->
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 12px;">
                                            <tr>
                                                <td>
                                                    <span style="display: inline-block; background-color: #ebf8ff; color: #2b6cb0; font-size: 11px; font-weight: 600; text-transform: uppercase; padding: 4px 8px; border-radius: 4px; letter-spacing: 0.5px;">
                                                        {category}
                                                    </span>
                                                    <span style="display: inline-block; background-color: {importance_bg}; color: {importance_color}; font-size: 11px; font-weight: 600; text-transform: uppercase; padding: 4px 8px; border-radius: 4px; letter-spacing: 0.5px; margin-left: 6px;">
                                                        Importance : {importance}
                                                    </span>
                                                </td>
                                            </tr>
                                        </table>

                                        <!-- Title -->
                                        <h2 style="margin: 0 0 10px 0; font-size: 18px; color: #1a202c; font-weight: 600; line-height: 1.3;">
                                            {title}
                                        </h2>

                                        <!-- Summary -->
                                        <p style="margin: 0 0 16px 0; font-size: 14px; color: #4a5568; line-height: 1.6;">
                                            {summary}
                                        </p>

                                        <!-- Call to Action Button -->
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                            <tr>
                                                <td style="border-radius: 4px; background-color: #3182ce;">
                                                    <a href="{url}" target="_blank" style="padding: 8px 14px; display: inline-block; color: #ffffff; font-size: 13px; font-weight: 600; text-decoration: none; border-radius: 4px;">
                                                        Lire l'article &rarr;
                                                    </a>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
        """

    # Footer
    contenu_html += """
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f7fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0; color: #a0aec0; font-size: 12px; line-height: 1.5;">
                            Bonne lecture,<br/>
                            <strong style="color: #718096;">TechDigest</strong>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """

    return contenu_html