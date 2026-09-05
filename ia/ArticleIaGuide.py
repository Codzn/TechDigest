from pydantic import BaseModel, Field

class ArticleIaGuide(BaseModel):

    summary: str = Field(description="A brief summary of the article.")

    category: str = Field(description="The category of the article.")

    importance: int = Field(description="The importance of the article.")