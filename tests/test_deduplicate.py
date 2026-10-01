from processors.deduplicate import remove_duplicates
from model.Article import Article

def test_remove_duplicates():
    article1 = Article(title="Sample Title", description="Sample Summary", url="http://example.com", score=0.9)
    article2 = Article(title="Sample Title", description="Sample Summary", url="http://example.org", score=0.8)  
    article3 = Article(title="Another Title", description="Another Summary", url="http://example.net", score=0.7)


    articles = [article1, article2, article3]

    removed_duplicates = remove_duplicates(articles)
    assert len(removed_duplicates) == 2
    print(removed_duplicates)

def test_keep_different_articles():
    article1 = Article(title="Unique Title 1", description="Summary 1", url="http://example.com", score=0.9)
    article2 = Article(title="Unique  5", description="Summary 2", url="http://example.org", score=0.8)

    articles = [article1, article2]

    keep_article = remove_duplicates(articles)
    assert len(keep_article) == 2

   
