from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.adapters.json import NewsApiAdapter
from newsagg.adapters.reddit import AsyncRedditAdapter
from newsagg.adapters.rss import AsyncRssAdapter
from newsagg.settings import RSS_DFT_NAMES


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
