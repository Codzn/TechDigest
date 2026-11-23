import json

from scripts.evaluate_filter import DATASET, evaluate, precision_recall


def test_filter_quality_does_not_regress():
    """Changing keywords or weights must not make the filter noticeably worse."""
    articles = json.loads(DATASET.read_text(encoding="utf-8"))["articles"]
    counts, _ = evaluate(articles)
    precision, recall = precision_recall(counts)

    assert precision >= 0.80
    assert recall >= 0.80
