from pydantic import UUID4
from sqlalchemy import select

from newsagg.config.database import SessionDep
from newsagg.models.user import User
from newsagg.schemas.user import UserInput


class UserRepository:
    """
    Repository class for handling users.
    """

    def __init__(self, session: SessionDep):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def is_superuser(self, user: User) -> bool:
        """
        Check if the user is a superuser.

        Args:
            user (User): The user instance.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return user.is_superuser

    async def create(self, data: UserInput, hashed_password: str) -> User:
        """
        Create a new user.

        Args:
            data (UserInput): The user data.
            hashed_password (str): The hashed password.

        Returns:
            User: The created user.
        """
        db_user = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def user_exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists by email.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none() is not None

    async def user_exists_by_username(self, username: str) -> bool:
        """
        Check if a user exists by username.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none() is not None

    async def get_user_by_email(self, email: str):
        """
        Get a user by email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User:
        """
        Get a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user.
        """
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement=statement)
        return result.scalar_one_or_none()

    async def get_user_object_by_id(self, _id: UUID4) -> User:
        """
        Get a user object by ID.

        Args:
            _id (UUID4): The ID of the user.

        Returns:
            Type[User]: The user instance.
        """
        result = await self.session.execute(select(User).where(User.id == _id))
        return result.scalar_one_or_none()

    async def user_exists_by_id(self, _id: UUID4) -> bool:
        """
        Check if a user exists by ID.

        Args:
            _id (UUID4): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        result = await self.session.execute(select(User).where(User.id == _id))
        return result.scalar_one_or_none() is not None

    async def delete_user(self, user: User) -> bool:
        """
        Delete a user.

        Args:
            user (Type[User]): The user instance.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        await self.session.delete(user)
        await self.session.commit()
        return True
