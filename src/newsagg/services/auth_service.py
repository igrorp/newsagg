import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from newsagg.config.database import SessionDep
from newsagg.models.user import User
from newsagg.services.exceptions import (
    IncorretUsernameOrPasswordError,
    TokenValidationError,
)
from newsagg.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TokenOAuth2BearerDep = Annotated[str, Depends(oauth2_scheme)]


class AuthService:
    """
    Service class for handling authentication-related operations.
    """

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    TOKEN_EXPIRES_MINS = int(os.getenv("TOKEN_EXPIRES_MINS"))  # type: ignore

    def __init__(self, session: SessionDep):
        """
        Initialize the service.

        Args:
            db (Session): Database session.
        """
        self.user_srvc = UserService(session)

    def decode_token(self, token: str) -> str:
        payload = jwt.decode(
            token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise TokenValidationError
        return username

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.TOKEN_EXPIRES_MINS
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode, key=self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_jwt

    async def get_current_user(self, token: TokenOAuth2BearerDep) -> User:
        try:
            username = self.decode_token(token=token)
        except JWTError:
            raise TokenValidationError

        user = await self.user_srvc.get_user_by_username(username=username)
        if user is None:
            raise TokenValidationError

        return user

    async def login(self, data: OAuth2PasswordRequestForm) -> Dict[Any, Any]:
        """
        User login.

        Args:
            data (OAuth2PasswordRequestForm): Login form data.

        Returns:
            dict: Token response.
        """
        user = await self.user_srvc.get_user_by_username(data.username)
        if user is None or not self.user_srvc.check_password(
            data.password, user
        ):
            raise IncorretUsernameOrPasswordError
        access_token = self.create_access_token(data={"sub": user.username})

        return {"access_token": access_token, "token_type": "bearer"}


class UserGetter:

    async def __call__(
        self, session: SessionDep, token: TokenOAuth2BearerDep
    ) -> User:
        return await AuthService(session=session).get_current_user(token=token)


UserAuthDep = Annotated[User, Depends(UserGetter())]
