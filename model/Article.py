from dataclasses import dataclass

@dataclass
class Article:
    title: str
    url: str
    description: str | None = None
    summary: str | None = None # Par défaut, le résumé est None si l'article n'a pas encore été résumé.
    score: float | None = None # Par défaut, le score est None si l'article n'a pas encore été évalué.


