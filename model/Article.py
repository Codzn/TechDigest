from dataclasses import dataclass

@dataclass
class Article:
    title: str
    url: str
    description: str | None = None
    summary: str | None = None # Par défaut, le résumé est None si l'article n'a pas encore été résumé.
    category: str | None = None # Par défaut, la catégorie est None si l'article n'a pas encore été catégorisé.
    importance: int | None = None # Par défaut, l'importance est None si l'article n'a pas encore été évalué.
    score: float | None = None # Par défaut, le score est None si l'article n'a pas encore été évalué.


