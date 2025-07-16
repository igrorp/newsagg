from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from newsagg.auth.exceptions import TokenValidationError
from newsagg.auth.token_encryption import ALGORITHM, SECRET_KEY
from newsagg.config.database import SessionDep
from newsagg.models.user import User
from newsagg.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenOAuth2BearerDep = Annotated[str, Depends(oauth2_scheme)]


class AuthService:
    """
    Service class for handling authentication-related operations.
    """

    def __init__(self, session: SessionDep):
        """
        Initialize the service.

        Args:
            db (Session): Database session.
        """
        self.user_repo = UserRepository(session)

    @staticmethod
    def decode_token(token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise TokenValidationError
        return username

    async def get_current_user(self, token: TokenOAuth2BearerDep) -> User:
        try:
            username = self.decode_token(token=token)
        except JWTError:
            raise TokenValidationError

        user = await self.user_repo.get_user_by_username(username=username)
        if user is None:
            raise TokenValidationError

        return user


class UserGetter:

    async def __call__(
        self, session: SessionDep, token: TokenOAuth2BearerDep
    ) -> User:
        return await AuthService(session=session).get_current_user(token=token)


UserAuthDep = Annotated[User, Depends(UserGetter())]
