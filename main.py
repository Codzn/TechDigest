from collectors.news_collector import get_news
from mail.email_generator import generate_email
from mail.email_sender import envoyer_veille_technologique
from processors.deduplicate import remove_duplicates
from processors.filtrage import filter_news, articles_sorted_by_score
from ia.summarizer import summarize_article

news = get_news()
cleaned_news = filter_news(news)
sorted_news = articles_sorted_by_score(cleaned_news)
# Supprimer les doublons
unique_articles = remove_duplicates(sorted_news)
summarized_articles = summarize_article(unique_articles)
html_content = generate_email(summarized_articles)
envoyer_veille_technologique(html_content)




