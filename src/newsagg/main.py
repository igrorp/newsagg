from typing import List

from fastapi import FastAPI, Query

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.adapters.json import NewsApiAdapter
from newsagg.adapters.reddit import AsyncRedditAdapter
from newsagg.adapters.rss import AsyncRssAdapter
from newsagg.service import NewsAggregator
from newsagg.settings import DFT_SOURCES, RSS_DFT_NAMES

app = FastAPI()


def get_sources(source: str) -> AsyncNewsSourceAdapter:

    if source == "news_data":
        return NewsApiAdapter()
    if "reddit:" in source:
        reddit_name = source.split(":")[1]
        return AsyncRedditAdapter(subreddit=reddit_name)
    elif source in RSS_DFT_NAMES:
        rss_url = RSS_DFT_NAMES.get(source)
        return AsyncRssAdapter(feed_url=rss_url, source_name=source)
    else:
        raise Exception(f"Could not find a valid adapter for source: {source}")


@app.get("/articles/")
async def get_articles(source: List[str] = Query(None)):
    if not source:
        source_objs = [get_sources(source=name) for name in DFT_SOURCES]
    else:
        source_objs = [get_sources(source=name) for name in source]

    aggregator = NewsAggregator(source_objs)

    articles = await aggregator.fetch_all_articles()
    return [article.model_dump() for article in articles]
