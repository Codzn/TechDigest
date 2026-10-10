from collectors.news_collector import get_news
from mail.email_generator import generate_email
from mail.email_sender import envoyer_veille_technologique
from processors.deduplicate import remove_duplicates
from processors.filtrage import filter_news, articles_sorted_by_score
from ia.summarizer import summarize_article
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("techdigest.log"), 
                              logging.StreamHandler()]
                    )
def main():
    """
    Fonction principale qui orchestre le processus de collecte, filtrage, déduplication, résumé et envoi d'articles.
    """
    news = get_news()
    if not news["articles"]:
        logging.error("No news articles found.")
        return
    
    logging.info(f"Fetched {len(news['articles'])} articles.")
    cleaned_news = filter_news(news)
    sorted_news = articles_sorted_by_score(cleaned_news)
    # Supprimer les doublons
    unique_articles = remove_duplicates(sorted_news)
    MAX_ARTICLES = 4
    top_articles = unique_articles[:MAX_ARTICLES]
    summarized_articles = summarize_article(top_articles)
    html_content = generate_email(summarized_articles)
    envoyer_veille_technologique(html_content)

if __name__ == "__main__":
    main()




