from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from collectors.news_collector import get_news
from model.Article import Article
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
    client = genai.Client(api_key=os.getenv("CLE_GEMINI"))

    for article in unique_articles:
        success = False  # Variable pour suivre si la génération a réussi
        
        #On crée une nouvelle session de chat vide pour chaque article.
        for i in range(3):  # Essayer jusqu'à 3 fois en cas d'erreur

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

                success = True
                break  # Sortir de la boucle si la génération est réussie

            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e): # Vérifier si l'erreur est un dépassement de quota
                    logging.error(f"Quota exceeded or rate limit reached: {e}. Retrying in 60 seconds...")
                    break  # Sortir de la boucle si le quota est dépassé
                if i < 2:  # Si ce n'est pas la dernière tentative
                    time.sleep(2 ** i)  # Attendre exponentiellement plus longtemps après chaque échec
                    print(f"Erreur lors de la génération du résumé pour l'article '{article.title}': {e}")

        if not success:
            print(f"Erreur : L'IA n'a pas pu générer de résumé pour l'article '{article.title}' après plusieurs tentatives.")
            continue  # Passer à l'article suivant

        json_brut = response.text
                
        if json_brut:
            # On force Pydantic à valider le JSON brut en utilisant le modèle ArticleIaGuide
            donnes_ia = ArticleIaGuide.model_validate_json(json_brut)
            #On range les données de l'article à partir de la réponse du modèle.
            article.summary = donnes_ia.summary
            article.category = donnes_ia.category
            article.importance = donnes_ia.importance

            print(f"Résumé de l'article '{article.title}':\n{article.summary}\n")
        else:
            print(f"Erreur : L'IA a renvoyé une réponse vide pour l'article '{article.title}'.")

            
    return unique_articles
