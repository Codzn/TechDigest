import google.genai as genai
import os
from dotenv import load_dotenv

from collectors.news_collector import get_news

"""
Ma fonction reçoit un ensemble d'articles filtrés et renvoie un résumé de ces articles sous forme de texte.
Elle utilise le modèle de génération de texte "gemini-1.5-flash" pour générer un résumé en français pour chaque article, en incluant le titre et la description de l'article. 
Le résumé est ensuite renvoyé sous forme de texte.

Elle enverra ensuite un email contenant le résumé généré à l'adresse e-mail spécifiée dans la variable d'environnement EMAIL_DESTINATAIRE.
"""

load_dotenv()

CLE_GEMINI = os.getenv("CLE_GEMINI")
genai.configure(api_key=CLE_GEMINI)

generator = genai.GenerativeModel("gemini-1.5-flash")

def summarize_article(unique_articles):
    """
    Récupère : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    Retour : Un résumé des articles sous forme de texte. 
    """
    texte = ""
    resume = ""
    prompt = "Tu es un expert en Systèmes d'Information. Pour chaque article ci-dessous, génère un titre en gras suivi d'un court paragraphe de résumé en français."
    for article in unique_articles:
        texte += article['title'] + "\n"
        if article['description'] is not None:
            texte += article['description'] + "\n"
    
    resume = generator.generate_content(prompt + "\n" + texte)
    return resume
