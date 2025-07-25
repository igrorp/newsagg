from fastapi import APIRouter

from .article_router import router as article_router
from .auth_router import router as auth_router
from .user_router import router as user_router

router = APIRouter(prefix="/api/v1")

router.include_router(article_router)
router.include_router(auth_router)
router.include_router(user_router)
