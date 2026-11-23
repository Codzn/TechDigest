# TechDigest

**An automated technology intelligence pipeline built with Python, NewsAPI, Gemini, and GitHub Actions.**

TechDigest collects technology news, filters articles relevant to information systems and digital transformation, removes duplicates, generates AI-powered summaries, and sends an HTML newsletter by email.

The project demonstrates a modular Python application integrating external APIs, data processing, AI-based content enrichment, automated testing, and scheduled execution.

## Objectives

The main objective is to automate technology monitoring across topics relevant to information systems and digital transformation, including:

- Artificial intelligence and machine learning
- Cloud computing
- Cybersecurity
- Data and analytics
- Enterprise Resource Planning (ERP)
- Customer Relationship Management (CRM)
- Product Lifecycle Management (PLM)
- Industry 4.0 and digital twins
- Industrial automation and connected systems

The application transforms raw news data into a curated email digest, reducing the effort required to monitor technology developments.

## Architecture

TechDigest follows a modular processing pipeline.

```text
NewsAPI
   |
   v
News collection
   |
   v
Relevance filtering and scoring
   |
   v
Duplicate detection
   |
   v
AI summarization and classification
   |
   v
HTML email generation
   |
   v
Gmail SMTP delivery
```

The application is orchestrated by `main.py`, while each module has a specific responsibility.

## Features

- **News collection:** Retrieves articles through NewsAPI.
- **Relevance filtering:** Uses normalized text, weighted keywords, and a configurable score threshold.
- **Duplicate detection:** Compares article titles using Jaccard similarity.
- **AI summarization:** Uses Google's Gemini API to generate French summaries.
- **Content classification:** Enriches articles with a category and an importance level.
- **Structured AI responses:** Uses Pydantic to validate the expected response schema.
- **HTML newsletter:** Generates an HTML email containing the selected articles.
- **Email delivery:** Sends the newsletter through Gmail SMTP.
- **Automated execution:** Uses GitHub Actions to run the pipeline on a schedule.
- **Automated testing:** Uses pytest to validate application behavior.

## Project Structure

```text
TechDigest/
├── collectors/
│   └── news_collector.py
├── processors/
│   ├── filtrage.py
│   └── deduplicate.py
├── ia/
│   ├── summarizer.py
│   └── ArticleIaGuide.py
├── model/
│   └── Article.py
├── mail/
│   ├── email_generator.py
│   └── send_newsletter.py
├── tests/
├── main.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

The `.github/workflows/` directory contains the GitHub Actions workflow used for automated execution.

## Processing Pipeline

### 1. News collection

`collectors/news_collector.py`

Retrieves news articles from NewsAPI.

### 2. Filtering and scoring

`processors/filtrage.py`

Normalizes article text, checks the required fields, and calculates a relevance score using weighted keywords.

Articles must exceed the configured score threshold to be retained.

### 3. Duplicate detection

`processors/deduplicate.py`

Compares normalized article titles using Jaccard similarity.

When sufficiently similar titles are found, the implementation retains the article with the highest relevance score.

### 4. AI summarization and classification

`ia/summarizer.py`

Calls the Gemini API to generate a French summary, category, and importance level.

The expected structured response is defined in `ia/ArticleIaGuide.py` and validated using Pydantic.

The application includes retry and error-handling logic for API failures. However, successful summarization depends on Gemini service availability and the applicable API quotas.

### 5. HTML generation

`mail/email_generator.py`

Generates an HTML newsletter from the processed articles.

Fallback values can be used when optional article fields, such as a summary or category, are unavailable.

### 6. Email delivery

`mail/send_newsletter.py`

Sends the generated HTML newsletter through Gmail SMTP.

The sender account must be configured with the required environment variables and an appropriate Gmail app password.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application development |
| NewsAPI | News collection |
| Requests | HTTP communication |
| Google Gemini API | Summarization and classification |
| Pydantic | Structured response validation |
| Dataclasses | Article data model |
| Regular expressions | Text normalization |
| Jaccard similarity | Duplicate detection |
| HTML | Newsletter generation |
| `smtplib` and `email.mime` | Email delivery |
| `python-dotenv` | Local environment configuration |
| pytest | Automated testing |
| GitHub Actions | Scheduled execution and CI automation |

## Installation

### Requirements

- Python 3.10 or newer
- A NewsAPI API key
- A Gemini API key
- A Gmail account configured for SMTP access

Clone the repository:

```bash
git clone https://github.com/Codzn/TechDigest.git
cd TechDigest
```

Create and activate a virtual environment.

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

### Local execution

Create a `.env` file in the project root.

```env
NEWS_API=your_newsapi_key
CLE_GEMINI=your_gemini_api_key

EMAIL_SENDER=your_address@gmail.com
PASS_EMAIL=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com
```

`RECIPIENT_EMAIL` is optional: if it is not set, the newsletter is sent to `EMAIL_SENDER`.

For Gmail SMTP, use an app password when required. Do not use your regular Gmail account password.

**Never commit `.env` or any real credentials to GitHub.**

### GitHub Actions secrets

For scheduled execution, configure the following repository secrets under:

`Settings → Secrets and variables → Actions`

| Secret | Purpose |
|---|---|
| `NEWS_API` | NewsAPI authentication |
| `CLE_GEMINI` | Gemini API authentication |
| `EMAIL_SENDER` | Gmail sender account |
| `PASS_EMAIL` | Gmail SMTP app password |
| `RECIPIENT_EMAIL` | Newsletter recipient |

The workflow passes these secrets to the application as environment variables with the same names.

## Usage

Run the complete pipeline locally:

```bash
python main.py
```

The application collects articles, filters them, removes duplicates, attempts AI enrichment, generates the HTML newsletter, and sends the email.

The newsletter's content depends on the articles returned by NewsAPI, the filtering rules, the availability of Gemini, and the applicable API quotas.

## Testing

Run the test suite:

```bash
pytest
```

The tests should validate application behavior without depending unnecessarily on live external APIs.

External service availability, API quotas, and SMTP delivery should be verified separately when performing an end-to-end test.

## Automated Execution

TechDigest uses GitHub Actions for automated execution.

The workflow supports:

- Scheduled execution
- Manual execution through `workflow_dispatch`
- Dependency installation
- Static checks with Flake8
- Automated tests with pytest
- Execution of `main.py`

The current schedule is configured in the workflow's cron expression.

For example:

```yaml
on:
  schedule:
    - cron: "0 8 * * 1"
  workflow_dispatch:
```

This example runs every Monday at 08:00 UTC, subject to GitHub Actions scheduling delays.

To change the frequency, update the cron expression in the workflow file.

Execution results and logs are available in the repository's **Actions** tab.

A successful workflow should confirm that the required steps completed successfully, including email delivery. Logging an error without propagating the failure may otherwise allow a workflow to appear successful.

## Reliability and Error Handling

TechDigest depends on external services, so a successful execution cannot be guaranteed on every run.

Potential failure scenarios include:

- NewsAPI errors or request limits
- Gemini service unavailability
- Gemini rate limits and quota exhaustion
- Invalid or incomplete AI responses
- SMTP connection interruptions
- Email delivery or spam-filtering issues

Gemini may return HTTP 503 when the service is temporarily overloaded or HTTP 429 when a rate limit or quota is exceeded.

The application includes retry and error-handling logic, but these mechanisms cannot eliminate external service failures.

Future reliability improvements include better recovery strategies, delivery verification, and more explicit reporting of partial failures.

## Security

- API keys and SMTP credentials are stored in environment variables.
- Local credentials are kept in `.env`, which must be excluded from version control.
- GitHub Actions credentials are configured through repository secrets.
- Credentials must never be written to application logs.
- The SMTP configuration uses encrypted communication with Gmail.

## What I Learned

Building TechDigest end to end taught me much more than writing a single script:

- **Designing a modular architecture.** I split the project into independent modules (collection, filtering, deduplication, AI summarization, email generation, delivery), each with one clear objective. This made each part easier to test, debug and improve without breaking the rest.
- **Working with unreliable external services.** The Gemini API regularly answered with `503 Service Unavailable` or `429 Too Many Requests`. I learned not to give up after the first failure: each article is retried up to 3 times with an exponential backoff (1 s, then 2 s), and the pipeline stops cleanly and keeps the summaries already generated when the quota is exhausted.
- **Measuring similarity between texts.** To detect the same news published by several outlets, I compute the **Jaccard similarity** between titles: the number of words they share divided by the total number of distinct words. Above 0.5, two articles are treated as duplicates and only the most relevant one is kept.
- **Scoring relevance with simple calculations.** Each article receives a weighted score: keywords count double in the title, and a bonus is added when several keywords appear together. Only articles above a threshold are kept.
- **Validating data.** Python dataclasses model an article, and Pydantic forces the AI to return a structured, validated JSON response (summary, category, importance) instead of free text.
- **Testing without calling real services.** The test suite uses mocks for SMTP and the Gemini API, so it runs quickly and for free.
- **Handling secrets properly.** API keys live in environment variables and GitHub Actions secrets. An early version wrote a log file containing a request URL with an API key, which taught me to never log credentials and to keep generated files out of version control.
- **Automating with CI/CD.** A GitHub Actions workflow checks the code, runs the tests and sends the newsletter every Monday without any manual action.

## Known Limitations

- Keyword-based filtering may miss relevant articles that use unexpected terminology.
- Jaccard similarity operates on article titles and cannot identify every semantic duplicate.
- AI-generated summaries may be incomplete or inaccurate and should not be treated as authoritative.
- Gemini service availability and quotas can limit the number of articles enriched during a run.
- SMTP acceptance does not guarantee inbox delivery; emails may be delayed, rejected, or classified as spam.
- Scheduled GitHub Actions executions may be delayed.

## Future Improvements

Potential extensions include:

- More robust handling of temporary API failures
- Improved observability and error reporting
- Better evaluation of filtering precision and recall
- Semantic search using embeddings
- Improved newsletter customization
- Cloud deployment using AWS Lambda
- Infrastructure as Code with Terraform
- Automated Cloud deployment through CI/CD

## License

This project is released under the [MIT License](LICENSE).
