from fastapi import APIRouter

from newsagg.config.database import SessionDep
from newsagg.schemas.user import UserInput
from newsagg.services.auth_service import UserAuthDep
from newsagg.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", status_code=201)
async def register(data: UserInput, session: SessionDep):
    """
    Register a new user.

    Args:
        data (UserIn): Details of the user to be registered.
        session (Session): Database session.

    return awaits:
        UserInDBBase: Details of the registered user.
    """
    _service = UserService(session)
    return await _service.create(data)


@router.get("/me", status_code=200)
async def get_me(user: UserAuthDep):
    """
    Retrieve information of the authenticated user.

    Args:
        user (UserIn): Current user's details.

    return awaits:
        UserIn: Details of the authenticated user.
    """
    return user


@router.delete("/me", status_code=204)
async def delete_me(session: SessionDep, user: UserAuthDep):
    """
    Delete the authenticated user.

    Args:
        user (UserIn): Current user's details.
        session (Session): Database session.

    return awaits:
        None
    """
    _service = UserService(session)
    return await _service.delete_user(user.id)
