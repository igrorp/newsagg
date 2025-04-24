from typing import List, Protocol

from newsagg.models import Article


class AsyncNewsSourceAdapter(Protocol):
    async def fetch_articles(self) -> List[Article]: ...
