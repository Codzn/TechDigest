TechDigest

TechDigest is a Python technology-watch script. It retrieves news, keeps articles relevant to information systems and digital transformation, removes duplicates, summarizes them with Gemini, and sends an HTML digest by email.

The project is designed as a simple pipeline: each module has one focused responsibility and `main.py` orchestrates the complete flow.

Goal

Receive a curated email containing articles about artificial intelligence, cloud computing, cybersecurity, ERP/CRM/PLM, Industry 4.0, digital twins, and related technology topics.

Architecture

NewsAPI
  -> get_news()
  -> filter_news()
  -> remove_duplicates()
  -> summarize_article()
  -> generate_email()
  -> envoyer_veille_technologique()
  -> e-mail HTML


Module Responsibility

Module -> Rôle 

collectors/news_collector.py -> Retrieves articles from NewsAPI through get_news().

processors/filtrage.py -> Cleans titles and descriptions, calculates a relevance score, and produces `Article` objects with `filter_news()`.

processors/duplicate.py -> Compares titles with Jaccard similarity and retains the highest-scored article when a duplicate is found.

model/Article.py -> Defines the `Article` dataclass: title, description, URL, score, summary, category, and importance.

ia/summarizer.py -> Calls Gemini to generate a French summary, category, and importance, then enriches each `Article`.

ia/ArticleIaGuide.py -> Defines the Pydantic schema expected from Gemini's structured response.

mail/email_generator.py -> Converts enriched articles into HTML through `generate_email()`.

mail/email_sender.py -> Sends the HTML content through Gmail SMTP with `envoyer_veille_technologique()`.

main.py -> Runs the pipeline in the correct order.

Pipeline

1. `get_news()` retrieves raw data from NewsAPI.
2. `filter_news()` skips articles without a title or description, normalizes text, and calculates a relevance score from weighted keywords.
3. Only articles whose score exceeds the threshold defined in `filtrage.py` are kept. Keywords found in a title carry more weight than keywords found in a description.
4. `remove_duplicates()` compares title word sets using Jaccard similarity. For sufficiently similar titles, the article with the highest score is kept.
5. `summarize_article()` enriches each article with `summary`, `category`, and `importance` through Gemini and a JSON response validated by Pydantic.
6. `generate_email()` creates the HTML newsletter.
7. `envoyer_veille_technologique()` sends the HTML through Gmail SMTP.

Installation

Requirements: Python 3.10 or newer, a NewsAPI account, a Gemini API key, and a Gmail account with an app password for SMTP sending.

git clone <REPOSITORY_URL>
cd TechDigest
python -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv google-genai pydantic

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Configuration

Create a `.env` file in the project root. Never commit it.

```env
# Adapt this name to the exact variable read by collectors/news_collector.py
NEWS_API_KEY=your_newsapi_key

CLE_GEMINI=your_gemini_key

EMAIL_USER=your_address@gmail.com
MDP_EMAIL=your_gmail_app_password
EMAIL_DESTINATAIRE=recipient@example.com
```

`EMAIL_DESTINATAIRE` may be omitted when the intended behavior is to send the digest to the sender address: `email_sender.py` then falls back to `EMAIL_USER`.

For Gmail, `MDP_EMAIL` must be an app password. Do not use the regular password of the account.

Add at least the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

Usage

From the project root:

```bash
python main.py
```

The script retrieves articles, runs the pipeline, generates HTML, and sends the email. Since SMTP sending has already been validated, it is recommended to send test digests to your own address first.

### Test the email without SMTP

The HTML generator can be tested separately with sample `Article` objects:

```python
contenu_html = generate_email(articles)

with open("test_email.html", "w", encoding="utf-8") as file:
    file.write(contenu_html)
```

Then open `test_email.html` in a browser. URLs stored in `Article` objects must be raw URLs, such as `https://example.com/article`, not Markdown links.

Diagnose an empty email

An empty email almost always means that the list passed to `generate_email()` is empty. It does not prove that there were no technology articles: count articles at every pipeline boundary.

Temporarily add this to `main.py`:

data = get_news()
print("NewsAPI:", len(data.get("articles", [])))

filtered_articles = filter_news(data)
print("After filtering:", len(filtered_articles))

unique_articles = remove_duplicates(filtered_articles)
print("After deduplication:", len(unique_articles))

Then, before generating the email:

summarized_articles = summarize_article(unique_articles)
print("After Gemini:", len(summarized_articles))

contenu_html = generate_email(summarized_articles)
print("HTML length:", len(contenu_html))

The first counter that reaches zero identifies the failing stage:

| Observation | Likely cause | Focused check |
| --- | --- | --- |
| `NewsAPI: 0` | Query, API key, NewsAPI parameters, or NewsAPI limit. | Print the raw response, its status, and the `status`, `totalResults`, and `articles` fields. |
| `After filtering: 0` | Threshold too high, keywords too restrictive, or missing titles/descriptions. | Print each article's title, normalized description, and score. |
| `After deduplication: 0` | A problem in the deduplication logic. | Test `remove_duplicates()` with two sample articles that have unrelated titles: both must remain. |
| `After Gemini: 0` | The function no longer returns the input list, or an error is hidden. | Check that `return unique_articles` is after the loop, not inside it. |
| Positive counters but nearly empty HTML | The wrong list is passed to `generate_email()`, or the HTML loop is incorrect. | Print `len(summarized_articles)` immediately before `generate_email()`. |

The most useful test is to print every article score before filtering. The current filter relies on specific expressions such as `artificial intelligence`, `cloud computing`, `cybersecurity`, `plm`, `erp`, or `digital twin`. A genuinely relevant technology article may be rejected when it uses different wording, such as a product or company name without one of these expressions.

Project structure

```text
TechDigest/
├── collectors/
│   └── news_collector.py
├── processors/
│   ├── filtrage.py
│   └── duplicate.py
├── ia/
│   ├── summarizer.py
│   └── ArticleIaGuide.py
├── model/
│   └── Article.py
├── mail/
│   ├── email_generator.py
│   └── email_sender.py
├── main.py
├── .env                 # local and ignored by Git
└── README.md
```

Technologies

- Python
- NewsAPI
- `requests` for HTTP requests
- Regular expressions (`re`) for text cleaning and keyword scoring
- `dataclasses` for the `Article` model
- Jaccard similarity and `set` for deduplication
- Gemini (`google-genai`) for summaries and structured classification
- Pydantic to validate Gemini's JSON response
- HTML and `email.mime` for the newsletter
- Gmail SMTP (`smtplib`) for email delivery
- `python-dotenv` for secret configuration

Possible improvements

- Add logging and explicit error handling for NewsAPI, Gemini, and SMTP failures.
- Test filtering and deduplication with fixed article datasets.
- Refine keywords, weights, and the threshold based on observed false positives and false negatives.
- Improve the HTML newsletter design.
- Add scheduled execution and avoid sending a digest when the selection is empty.
- Limit the number of articles sent to control Gemini call time and cost.

Known limitations

- Keyword filtering does not understand article meaning: it can produce false positives and reject relevant articles written with different terminology.
- Jaccard similarity compares title words only, so it cannot identify all duplicates phrased very differently.
- Summarization and categorization depend on an external service and can fail or produce output that should be reviewed.
