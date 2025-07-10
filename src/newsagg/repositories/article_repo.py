from typing import List, Optional

from sqlalchemy import select

from newsagg.config.database import SessionDep
from newsagg.models.article import Article
from newsagg.schemas.article import ArticleORM


class ArticleRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    async def get_all_articles(self) -> List[Article]:
        result = await self.session.execute(select(ArticleORM))
        articles = result.scalars().all()
        return [
            Article(
                title=a.title,
                link=a.link,
                publishedAt=a.published_at,
                source=a.source,
                summary=a.summary,
                retrievedAt=a.retrieved_at,
            )
            for a in articles
        ]

    async def get_article_by_id(self, article_id: int) -> Optional[Article]:
        result = await self.session.execute(
            select(ArticleORM).where(ArticleORM.id == article_id)
        )
        article = result.scalar_one_or_none()
        if article:
            return Article(
                title=article.title,
                link=article.link,
                publishedAt=article.published_at,
                source=article.source,
                summary=article.summary,
                retrievedAt=article.retrieved_at,
            )
        return None

    async def create_article(self, article: Article) -> Article:
        db_article = ArticleORM(
            title=article.title,
            link=article.link,
            published_at=article.publishedAt,
            source=article.source,
            summary=article.summary,
            retrieved_at=article.retrievedAt,
        )
        self.session.add(db_article)
        await self.session.commit()
        await self.session.refresh(db_article)
        return article

    async def update_article(
        self, article_id: int, article: Article
    ) -> Optional[Article]:
        result = await self.session.execute(
            select(ArticleORM).where(ArticleORM.id == article_id)
        )
        db_article = result.scalar_one_or_none()
        if not db_article:
            return None
        db_article.title = article.title
        db_article.link = article.link
        db_article.published_at = article.publishedAt
        db_article.source = article.source
        db_article.summary = article.summary
        db_article.retrieved_at = article.retrievedAt
        await self.session.commit()
        await self.session.refresh(db_article)
        return article

    async def delete_article(self, article_id: int) -> bool:
        result = await self.session.execute(
            select(ArticleORM).where(ArticleORM.id == article_id)
        )
        db_article = result.scalar_one_or_none()
        if not db_article:
            return False
        await self.session.delete(db_article)
        await self.session.commit()
        return True
