import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

CLE_GEMINI = os.getenv("CLE_GEMINI")
genai.configure(api_key=CLE_GEMINI)

generator = genai.GenerativeModel("gemini-1.5-flash")
def summarize_article(articles):
    """
    Récupère : Les articles filtrés dans une liste en fonction des mots-clés définis dans SI_KEYWORDS.
    Retour : Un résumé des articles sous forme de texte. 
    """
    texte = ""
    resume = ""
    prompt = "Tu es un expert en Systèmes d'Information. Pour chaque article ci-dessous, génère un titre en gras suivi d'un court paragraphe de résumé en français."
    for article in articles:
        texte += article['title'] + "\n"
        if article['description'] is not None:
            texte += article['description'] + "\n"
    
    resume = generator.generate_content(prompt + "\n" + texte)
    return resume
