from processors.filtrage import filter_news, articles_sorted_by_score, calculate_score

def test_filterage():
    test_data = {
        "articles": [
            {
                "title": "IA and Machine Learning: The Future of Data Science",
                "description": "This is an article about ia and machine learning and data science.",
                "url": "https://www.bbc.com/news/articles/cqx2z23xj555o"
            },
            {
                "title": "Why did an OpenAI system hack Australia's SI system?",
                "description": "Why did an OpenAI system hack Australia's health system - and can it be stopped in the future? By an Ai researcher and a cybersecurity expert.",
                "url": "https://www.bbc.com/news/articles/cw24jm9rryy3o"
            },
            {
                "title": "",
                "description": "",
                "url": ""
            }
        ]
    }

    score = calculate_score("IA and Machine Learning: The Future of Data Science", "This is an article about ia and machine learning and data science.")
    assert score > 4  # Vérifie que le score est supérieur à 4 pour l'article sur l'IA et le machine learning

    score2 = calculate_score("Why did an OpenAI system hack Australia's SI system?", "Why did an OpenAI system hack Australia's health system - and can it be stopped in the future? By an Ai researcher and a cybersecurity expert.")
    assert score2 > 4  # Vérifie que le score est supérieur à 4

    filtered_articles = filter_news(test_data)
    assert len(filtered_articles) == 2
    assert filtered_articles[0].title == "ia and machine learning: the future of data science"
    assert filtered_articles[1].title == "why did an openai system hack australia's si system?"

    filtered_articles_sorted = articles_sorted_by_score(filtered_articles)
    assert filtered_articles_sorted[0].score >= filtered_articles_sorted[1].score



