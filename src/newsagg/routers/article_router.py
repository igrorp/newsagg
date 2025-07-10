from typing import List, Optional

from fastapi import APIRouter

from newsagg.config.database import SessionDep
from newsagg.models.article import Article
from newsagg.repositories.article import ArticleRepository

router = APIRouter(prefix="/articles")


@router.get("")
async def get_all_articles(session: SessionDep) -> List[Article]:
    _service = ArticleRepository(session=session)
    return await _service.get_all_articles()


@router.get("/{article_id}/")
async def get_article_by_id(
    session: SessionDep, article_id: int
) -> Optional[Article]:
    _service = ArticleRepository(session=session)
    return await _service.get_article_by_id(article_id=article_id)


@router.post("")
async def create_article(session: SessionDep, article: Article) -> Article:
    _service = ArticleRepository(session=session)
    return await _service.create_article(article=article)


@router.put("/{article_id}/")
async def update_article(
    session: SessionDep, article_id: int, article: Article
) -> Optional[Article]:
    _service = ArticleRepository(session=session)
    return await _service.update_article(article=article, article_id=article_id)


@router.delete("/{article_id}")
async def delete_article(session: SessionDep, article_id: int) -> bool:
    _service = ArticleRepository(session=session)
    return await _service.delete_article(article_id=article_id)
