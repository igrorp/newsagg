from datetime import datetime

import aiohttp

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.models import Article


class AsyncRedditAdapter(AsyncNewsSourceAdapter):
    def __init__(self, subreddit: str):
        self.api_url = f"https://www.reddit.com/r/{subreddit}/.json"
        self.source_name = f"reddit:{subreddit}"

    async def fetch_articles(self) -> list[Article]:
        headers = {"User-Agent": "newsagg-bot/0.1"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.api_url) as resp:
                data = await resp.json()

        return [
            Article(
                title=post["data"]["title"],
                link=f"https://reddit.com{post['data']['permalink']}",
                publishedAt=datetime.fromtimestamp(post["data"]["created_utc"]),
                source=self.source_name,
                summary=post["data"].get("selftext", "")[:200],
                retrievedAt=datetime.now(),
            )
            for post in data["data"]["children"]
        ]
