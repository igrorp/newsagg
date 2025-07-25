from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from newsagg.config.database import SessionDep
from newsagg.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=201)
async def login(
    session: SessionDep, data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login user.

    Args:
        data (OAuth2PasswordRequestForm): User credentials.
        session (Session): Database session.

    return awaits:
        None
    """
    _service = AuthService(session)
    return await _service.login(data)
