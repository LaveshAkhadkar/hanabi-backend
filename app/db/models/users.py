from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False


class SignupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str
