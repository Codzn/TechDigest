from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from collectors.news_collector import get_news
from model.Article import Article

"""
Ma fonction reçoit un ensemble d'articles filtrés et renvoie un résumé de ces articles sous forme de texte.
Elle utilise le modèle de génération de texte "gemini-1.5-flash" pour générer un résumé en français pour chaque article, en incluant le titre et la description de l'article. 
Le résumé est ensuite renvoyé sous forme de texte.

Elle enverra ensuite un email contenant le résumé généré à l'adresse e-mail spécifiée dans la variable d'environnement EMAIL_DESTINATAIRE.
"""

load_dotenv()
client = genai.Client(api_key=os.getenv("CLE_GEMINI"))


def summarize_article(unique_articles):
    """
    Récupère : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    Retour : Un résumé des articles sous forme de texte. 
    """
    summaries = []
    config = types.GenerateContentConfig(
        system_instruction="""You are an expert in Information Systems. Summarise the article in French in 1 paragraph of 4 to 6 sentences.
        Keep the important information, the context and the main consequences.
        The summary must be detailed enough for a person to understand the interest of the article without reading the original article.
    """)

    for article in unique_articles:
        #On crée une nouvelle session de chat vide pour chaque article.
        chat = client.chats.create(model="gemini-3.6-flash", config=config)

        prompt = f"Title: {article.title}\nDescription: {article.description}\nURL: {article.url}"
        response = chat.send_message(prompt)

        print(f"Résumé de l'article '{article.title}':\n{response.text}\n")

        article.summary = response.text

    return unique_articles
