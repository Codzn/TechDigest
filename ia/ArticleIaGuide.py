from typing import Literal

from pydantic import BaseModel, Field

class ArticleIaGuide(BaseModel):

    summary: str = Field(description="A brief summary of the article.")

    category: str = Field(description="The category of the article.")

    importance: Literal["Faible", "Moyenne", "Élevée"] = Field(
        description="The importance of the article for an Information Systems professional."
    )