from fastapi import HTTPException
from pydantic import UUID4

from newsagg.config.database import SessionDep
from newsagg.models.article import Article
from newsagg.models.user import User
from newsagg.repositories.article_repo import ArticleRepository
from newsagg.repositories.user_repo import UserRepository
from newsagg.services.auth_service import UserAuthDep


class ArticleService:
    """
    Service class for handling Article operations.
    """

    def __init__(self, session: SessionDep):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = ArticleRepository(session)
        self.user_repo = UserRepository(session)

    async def create(self, data: Article, user: User) -> Article:
        """
        Create a new Article.

        Args:
            data (Article): Article data.

        Returns:
            Article: Created Article data.
        """
        if not self.user_repo.is_superuser(user=user):
            raise HTTPException(
                status_code=403, detail="Only superusers can create articles"
            )
        article = await self.repository.create_article(data)
        return article

    async def delete(self, _id: UUID4, user: UserAuthDep) -> bool:
        """
        Delete a Article.

        Args:
            _id (UUID4): Article ID.

        Returns:
            bool: True if the Article is successfully deleted, False otherwise.
        """
        if not self.user_repo.is_superuser(user=user):
            raise HTTPException(
                status_code=403, detail="Only superusers can create articles"
            )
        article = await self.repository.get_article_by_id(_id)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        await self.repository.delete_article(article)
        return True

    async def update(
        self, _id: UUID4, data: Article, user: UserAuthDep
    ) -> Article:
        """
        Update an existing Article.

        Args:
            _id (UUID4): Article ID.
            data (Article): Updated Article data.

        Returns:
            Article: Updated Article data.
        """
        if not self.user_repo.is_superuser(user=user):
            raise HTTPException(
                status_code=403, detail="Only superusers can create articles"
            )
        article = await self.repository.get_article_by_id(_id)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        updated_article = await self.repository.update_article(article, data)
        return updated_article

    async def get_by_id(self, _id: UUID4) -> Article:
        """
        Get an Article by ID.

        Args:
            _id (UUID4): Article ID.

        Returns:
            Article: Article data.
        """
        article = await self.repository.get_article_by_id(_id)
        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

    async def get_all(self) -> list[Article]:
        """
        Get all Articles.

        Returns:
            list[Article]: List of all Article objects.
        """
        articles = await self.repository.get_all_articles()
        return articles
