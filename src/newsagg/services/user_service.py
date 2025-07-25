from typing import ClassVar, Optional

from passlib.context import CryptContext
from pydantic import UUID4

from newsagg.config.database import SessionDep
from newsagg.models.user import User
from newsagg.repositories.user_repo import UserRepository
from newsagg.schemas.user import UserBase, UserInput
from newsagg.services.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)


class UserService:
    """
    Service class for handling user-related operations.
    """

    PWD_CONTEXT: ClassVar[CryptContext] = CryptContext(
        schemes=["bcrypt"], deprecated="auto"
    )

    def __init__(self, session: SessionDep):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = UserRepository(session)

    def get_password_hash(self, password: str) -> str:
        """Hash the password using bcrypt.

        Args:
            password (str): the password to hash.

        Returns:
            str: the hashed passoword.
        """
        return self.PWD_CONTEXT.hash(password)

    def check_password(self, password: str, user: User) -> bool:
        """Check if the provided password matches the hashed password.

        Args:
            password (str): the password to check.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.PWD_CONTEXT.verify(password, user.hashed_password)

    async def create(self, data: UserInput) -> UserBase:
        """
        Create a new user.

        Args:
            data (UserInput): User data.

        Returns:
            User: Created user data.
        """
        if await self.repository.user_exists_by_email(data.email):
            raise EmailAlreadyExistsError
        if await self.repository.user_exists_by_username(data.username):
            raise UsernameAlreadyExistsError

        hashed_password = self.get_password_hash(data.password)
        user = await self.repository.create(data, hashed_password)

        return UserBase(**user.__dict__)

    async def is_superuser(self, _id: UUID4) -> bool:
        """
        Check if the user is a superuser.

        Args:
            _id (UUID4): User ID.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        if not await self.repository.user_exists_by_id(_id):
            raise UserNotFoundError

        user = self.repository.get_user_object_by_id(_id)
        return user.is_superuser

    async def delete_user(self, _id: UUID4) -> bool:
        """
        Delete a user.

        Args:
            _id (UUID4): User ID.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.
        """
        if not await self.repository.user_exists_by_id(_id):
            raise UserNotFoundError

        user = await self.repository.get_user_object_by_id(_id)
        await self.repository.delete_user(user)
        return True

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by username.

        Args:
            username (str): The username to search for.

        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        user = await self.repository.get_user_by_username(username)
        return user
