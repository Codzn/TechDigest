from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from ia.ArticleIaGuide import ArticleIaGuide
import time
import logging

"""
Ma fonction reçoit un ensemble d'articles filtrés et renvoie un résumé de ces articles sous forme de texte.
Elle utilise le modèle de génération de texte "gemini-1.5-flash" pour générer un résumé en français pour chaque article, en incluant le titre et la description de l'article. 
Le résumé est ensuite renvoyé sous forme de texte.

Elle enverra ensuite un email contenant le résumé généré à l'adresse e-mail spécifiée dans la variable d'environnement EMAIL_DESTINATAIRE.
"""

load_dotenv()

def summarize_article(unique_articles):
    """
    Récupère : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    Retour : Un résumé des articles sous forme de texte. 
    """
    api_key = os.getenv("CLE_GEMINI")

    if not api_key:
        raise ValueError("La clé d'API Gemini n'est pas définie dans les variables d'environnement.")
    
    client = genai.Client(api_key=api_key)
    summarized_articles = []
    
    for article in unique_articles:
        
        #On crée une nouvelle session de chat vide pour chaque article.
        for attempt in range(3):  # Essayer jusqu'à 3 fois en cas d'erreur

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"Title: {article.title}\nDescription: {article.description}\nURL: {article.url}",
                    config=types.GenerateContentConfig(
                        system_instruction="""You are an expert in Information Systems. Summarise the article in French in 1 paragraph of 4 to 6 sentences.
                                Keep the important information, the context and the main consequences.
                                The summary must be detailed enough for a person to understand the interest of the article without reading the original article.
                            """,
                        response_mime_type="application/json",
                        response_schema=ArticleIaGuide,
                    ),
                )

                if not response or not response.text:
                    raise ValueError(f"Received empty response for article '{article.title}'.")

                data = ArticleIaGuide.model_validate_json(response.text) # Valider et convertir la réponse JSON en un objet ArticleIaGuide

                article.summary = data.summary
                article.category = data.category
                article.importance = data.importance

                summarized_articles.append(article)
                logging.info(f"Resume of the article '{article.title}'")

                break  # Sortir de la boucle si la génération est réussie

            except Exception as e:
                error_message = str(e)
                if ("429" in error_message or "RESOURCE_EXHAUSTED" in error_message):  # Vérifier si l'erreur est un dépassement de quota
                    logging.error(f"Quota exceeded or rate limit reached: {e}.")
                    return summarized_articles  # Retourner les articles déjà résumés avant le dépassement de quota
                if attempt < 2:  # Si ce n'est pas la dernière tentative
                    delay = 2 ** attempt  # Attendre exponentiellement plus longtemps après chaque échec
                    logging.warning(f"Error during the generation of the resume '{article.title}': {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logging.exception(f"Failed to generate summary for article '{article.title}' after 3 attempts: {e}")

    logging.info(f"Summarized {len(summarized_articles)} out of {len(unique_articles)} articles.")

            
    return summarized_articles
