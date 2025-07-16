from typing import List, Optional

from fastapi import APIRouter

from newsagg.config.database import SessionDep
from newsagg.models.article import Article
from newsagg.services.article_service import ArticleService
from newsagg.services.auth_service import UserAuthDep

router = APIRouter(prefix="/article")


@router.get("")
async def get_all_articles(session: SessionDep) -> List[Article]:
    _service = ArticleService(session=session)
    return await _service.get_all()


@router.get("/{article_id}/")
async def get_article_by_id(
    session: SessionDep, article_id: int
) -> Optional[Article]:
    _service = ArticleService(session=session)
    return await _service.get_by_id(_id=article_id)


@router.post("")
async def create_article(
    session: SessionDep, article: Article, user: UserAuthDep
) -> Article:
    _service = ArticleService(session=session)
    return await _service.create(data=article, user=user)


@router.put("/{article_id}/")
async def update_article(
    session: SessionDep, article_id: int, article: Article, user: UserAuthDep
) -> Optional[Article]:
    _service = ArticleService(session=session)
    return await _service.update(data=article, _id=article_id, user=user)


@router.delete("/{article_id}")
async def delete_article(
    session: SessionDep, article_id: int, user: UserAuthDep
) -> bool:
    _service = ArticleService(session=session)
    return await _service.delete(_id=article_id, user=user)
