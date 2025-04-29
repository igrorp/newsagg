from datetime import datetime
from typing import List, Optional

import httpx

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.models import Article


class NewsApiAdapter(AsyncNewsSourceAdapter):
    BASE_URL = "https://newsdata.io/api/1/latest"

    def __init__(
        self,
        country: str = "br",
        category: Optional[str] = None,
        source_name: str = "news_data",
    ):
        self.country = country
        self.category = category
        self.source_name = source_name

    async def fetch_articles(self) -> List[Article]:
        params = {
            "apiKey": "pub_828473085d032723967252d7df231f9f05bf8",
            "country": self.country,
        }
        if self.category:
            params["category"] = self.category

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        articles = []
        for item in data.get("results", []):
            articles.append(
                Article(
                    title=item["title"],
                    link=item["source_url"],
                    summary=item.get("description") or "",
                    source=self.source_name,
                    publishedAt=datetime.fromisoformat(item["pubDate"]),
                    retrievedAt=datetime.now(),
                )
            )

        return articles
