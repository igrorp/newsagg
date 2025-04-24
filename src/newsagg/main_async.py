import asyncio

from newsagg.adapters.reddit import AsyncRedditAdapter
from newsagg.adapters.rss import AsyncRssAdapter


async def main():
    sources = [
        AsyncRssAdapter("https://g1.globo.com/rss/g1/", "G1"),
        AsyncRedditAdapter("worldnews"),
    ]

    all_articles = await asyncio.gather(*[s.fetch_articles() for s in sources])
    for article in all_articles[0][:5]:  # print a few from G1
        print(
            f"{article.publishedAt:%Y-%m-%d} "
            "{article.retrievedAt:%Y-%m-%d} | "
            "{article.source} | {article.title}"
        )
    for article in all_articles[1][:5]:  # print a few from Reddit
        print(
            f"{article.publishedAt:%Y-%m-%d} "
            "{article.retrievedAt:%Y-%m-%d} | "
            "{article.source} | {article.title}"
        )


if __name__ == "__main__":
    asyncio.run(main())
