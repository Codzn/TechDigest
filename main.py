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
    try:
        news = get_news()
        if not news["articles"]:
            logging.error("No news articles found.")
            return
        
        logging.info(f"Fetched {len(news['articles'])} articles.")
        
        cleaned_news = filter_news(news)
        if not cleaned_news:
            logging.warning("No articles left after filtering.")
            return
        
        sorted_news = articles_sorted_by_score(cleaned_news)
        unique_articles = remove_duplicates(sorted_news)
        
        if not unique_articles:
            logging.warning("No unique articles found after deduplication.")
            return
        
        # Selectionner les 4 articles les plus pertinents
        MAX_ARTICLES = 4
        top_articles = unique_articles[:MAX_ARTICLES]
        logging.info(f"Selected top {len(top_articles)} articles for summarization.")
        
        summarized_articles = summarize_article(top_articles)
        if not summarized_articles:
            logging.warning("No articles were summarized.")
            raise RuntimeError("No articles were summarized; newsletter was not sent")
        html_content = generate_email(summarized_articles)
        if not html_content:
            logging.error("Failed to generate email content.")
            raise RuntimeError("Failed to generate email content.")
        envoyer_veille_technologique(html_content)
        logging.info("Pipeline TechDigest completed.")
    except Exception:
        logging.exception("An error occurred during the TechDigest pipeline.")
        raise

if __name__ == "__main__":
    main()




