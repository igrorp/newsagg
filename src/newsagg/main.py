from typing import List, Optional

from fastapi import FastAPI, Query

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.adapters.reddit import AsyncRedditAdapter
from newsagg.adapters.rss import AsyncRssAdapter
from newsagg.service import NewsAggregator
from newsagg.settings import DFT_SOURCES, RSS_DFT_NAMES

app = FastAPI()


def get_source_url(source: str) -> Optional[str]:

    rss_url = RSS_DFT_NAMES.get(source)
    if rss_url is None:
        raise Exception(f"Could not find a valid URL for source: {source}")

    return rss_url


def get_sources(source: str) -> AsyncNewsSourceAdapter:

    if "reddit:" in source:
        reddit_name = source.split(":")[1]
        return AsyncRedditAdapter(subreddit=reddit_name)
    else:
        url = get_source_url(source=source)
        return AsyncRssAdapter(feed_url=url, source_name=source)


@app.get("/articles/")
async def get_articles(source: List[str] = Query(None)):
    if not source:
        source_objs = [get_sources(source=name) for name in DFT_SOURCES]
    else:
        source_objs = [get_sources(source=name) for name in source]

    aggregator = NewsAggregator(source_objs)

    articles = await aggregator.fetch_all_articles()
    return [article.model_dump() for article in articles]
