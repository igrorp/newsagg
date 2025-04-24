import re
from datetime import datetime

import aiohttp
import feedparser

from newsagg.adapters.base import AsyncNewsSourceAdapter
from newsagg.models import Article


class AsyncRssAdapter(AsyncNewsSourceAdapter):
    def __init__(self, feed_url: str, source_name: str):
        self.feed_url = feed_url
        self.source_name = source_name

    async def fetch_articles(self) -> list[Article]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.feed_url) as resp:
                raw_feed = await resp.read()

        parsed = feedparser.parse(raw_feed)

        to_remove = []

        for entry in parsed.entries:

            title = entry.get("title")
            if any(
                (
                    "Assista ao" in title,
                    "Vídeos do g1" in title,
                    "EPTV 2 Campinas ao vivo" in title,
                    "EPTV2" in title,
                    "VÍDEOS:" in title,
                )
            ):
                to_remove.append(entry)

        [parsed.entries.remove(entry) for entry in to_remove]

        for entry in parsed.entries:

            summary = entry.get("summary")
            processed_summary = re.sub(r"\u003C(.)+\u003E", "", summary)
            processed_summary = re.sub(
                r"✅ Clique (.)+\.", "", processed_summary
            )
            processed_summary = re.sub(
                r"(\.)([^\.]*?WhatsApp)", r"\1", processed_summary
            )
            processed_summary = processed_summary.replace('"', '''"''')
            processed_summary = re.sub(
                r"(?<=\S)\n(?=\S)", " ", processed_summary
            )
            processed_summary = processed_summary.replace("\n", "").strip()
            entry["summary"] = processed_summary

        return [
            Article(
                title=entry.title,
                link=entry.link,
                publishedAt=datetime(*entry.published_parsed[:6]),
                source=self.source_name,
                summary=entry.get("summary"),
                retrievedAt=datetime.now(),
            )
            for entry in parsed.entries
        ]
