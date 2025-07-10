from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    link: str
    publishedAt: datetime
    source: str
    summary: str | None = None
    retrievedAt: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "publishedAt": "published_at",
            "retrievedAt": "retrieved_at",
        }
