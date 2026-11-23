"""
Evaluate the relevance filter on a hand-labelled dataset.

Each article in data/test_articles.json has an `expected_relevant` label.
The script runs the same scoring as the pipeline and reports:
- precision: among the articles kept, how many were really relevant
- recall: among the relevant articles, how many were kept

Usage:
    python scripts/evaluate_filter.py
"""
import json
from pathlib import Path

from processors.filtrage import SCORE_THRESHOLD, calculate_score, clean_text

DATASET = Path(__file__).resolve().parent.parent / "data" / "test_articles.json"


def evaluate(articles):
    """Return the confusion counts and the misclassified articles."""
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    errors = []
    for article in articles:
        score = calculate_score(clean_text(article["title"]), clean_text(article["description"]))
        predicted = score > SCORE_THRESHOLD
        expected = article["expected_relevant"]
        if predicted and expected:
            counts["tp"] += 1
        elif predicted and not expected:
            counts["fp"] += 1
            errors.append(("false positive", score, article["title"]))
        elif expected:
            counts["fn"] += 1
            errors.append(("false negative", score, article["title"]))
        else:
            counts["tn"] += 1
    return counts, errors


def precision_recall(counts):
    kept = counts["tp"] + counts["fp"]
    relevant = counts["tp"] + counts["fn"]
    precision = counts["tp"] / kept if kept else 0.0
    recall = counts["tp"] / relevant if relevant else 0.0
    return precision, recall


def main():
    articles = json.loads(DATASET.read_text(encoding="utf-8"))["articles"]
    counts, errors = evaluate(articles)
    precision, recall = precision_recall(counts)

    print(f"Articles evaluated: {len(articles)}")
    print(f"Precision: {precision:.0%}  |  Recall: {recall:.0%}")
    print(f"Kept correctly: {counts['tp']}  |  Rejected correctly: {counts['tn']}")
    print(f"False positives: {counts['fp']}  |  False negatives: {counts['fn']}")
    if errors:
        print("\nMisclassified articles:")
        for kind, score, title in errors:
            print(f"  - [{kind}, score {score}] {title}")


if __name__ == "__main__":
    main()
