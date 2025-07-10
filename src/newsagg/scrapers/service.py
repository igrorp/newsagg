import asyncio
from typing import List

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.models import Article


class NewsAggregator:
    def __init__(self, sources: List[AsyncNewsSourceAdapter]):
        self.sources = sources

    async def fetch_all_articles(self) -> List[Article]:
        results = await asyncio.gather(
            *[src.fetch_articles() for src in self.sources]
        )

        all_articles = [
            article
            for source_articles in results
            for article in source_articles
        ]
        all_articles.sort(key=lambda a: a.publishedAt, reverse=True)

        return all_articles
