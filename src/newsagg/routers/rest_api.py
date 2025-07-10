from fastapi import APIRouter

from .article import router as article_router

router = APIRouter(prefix="/api/v1")

router.include_router(article_router)
