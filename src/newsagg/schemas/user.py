from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserInput(UserBase):
    password: str


class UserDB(UserInput):
    is_superuser: bool = False
    is_active: bool = True
