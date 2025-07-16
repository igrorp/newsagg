from typing import Any, Dict

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4

from newsagg.auth.email_validation import validate_email
from newsagg.auth.password_hashing import get_password_hash, pwd_context
from newsagg.auth.password_validation import validate_password
from newsagg.auth.token_encryption import create_access_token
from newsagg.config.database import SessionDep
from newsagg.repositories.user_repo import UserRepository
from newsagg.schemas.user import UserBase, UserInput
from newsagg.services.exceptions import (
    EmailAlreadyExistsError,
    IncorretUsernameOrPasswordError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)


class UserService:
    """
    Service class for handling user-related operations.
    """

    def __init__(self, session: SessionDep):
        """
        Initialize the service.

        Args:
            session (Session): Database session.
        """
        self.repository = UserRepository(session)

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

        violations = validate_password(data.password)
        if violations:
            raise HTTPException(
                status_code=400,
                detail=[v.ERROR_MSG for v in violations],
            )
        validate_email(data.email)

        hashed_password = get_password_hash(data.password)
        user = await self.repository.create(data, hashed_password)
        return UserBase(**user.__dict__)

    async def login(self, data: OAuth2PasswordRequestForm) -> Dict[Any, Any]:
        """
        User login.

        Args:
            data (OAuth2PasswordRequestForm): Login form data.

        Returns:
            dict: Token response.
        """
        user = await self.repository.get_user_by_username(data.username)
        if not user or not pwd_context.verify(
            data.password, user.hashed_password
        ):
            raise IncorretUsernameOrPasswordError
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

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
