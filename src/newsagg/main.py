from fastapi import FastAPI

from newsagg.adapters.reddit import AsyncRedditAdapter
from newsagg.adapters.rss import AsyncRssAdapter
from newsagg.service import NewsAggregator
from newsagg.settings import FOLHA_URL, G1_URL, NYT_URL

app = FastAPI()


@app.get("/articles")
async def get_articles():

    sources = [
        AsyncRssAdapter(G1_URL, "G1"),
        AsyncRssAdapter(NYT_URL, "NYT"),
        AsyncRedditAdapter("worldnews"),
        AsyncRssAdapter(FOLHA_URL, "Folha"),
    ]

    aggregator = NewsAggregator(sources)

    articles = await aggregator.fetch_all_articles()
    return [article.model_dump() for article in articles]
