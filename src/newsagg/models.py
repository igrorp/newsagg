from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    link: str
    publishedAt: datetime
    source: str
    summary: str | None = None
    retrievedAt: datetime
