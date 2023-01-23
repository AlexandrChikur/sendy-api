from pydantic import EmailStr
from pydantic.class_validators import validator

from app.models.domain.users import User
from app.models.schemas.jwt import JWTToken
from app.models.schemas.rwschema import RWSchema


class UserInLogin(RWSchema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str

    @validator("username")
    def check_username_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username length should be greater than 3 characters")
        if len(v) > 16:
            raise ValueError("Username length shouldn't be greater than 16 characters")
        return v

    @validator("email")
    def check_email_length(cls, v: str) -> str:
        if len(v) > 64:
            raise ValueError("Email length shouldn't be greater than 64 characters")
        return v

    @validator("password")
    def check_password_strength(cls, pwd: str) -> str:
        if len(pwd) < 6:
            raise ValueError("Password length should be at least 6")
        if not any(char.isdigit() for char in pwd):
            raise ValueError("Password should have at least one numeral")
        if not any(char.isupper() for char in pwd):
            raise ValueError("Password should have at least one uppercase letter")
        return pwd


class UserWithToken(RWSchema, User):
    token: JWTToken


class UserInResponse(RWSchema, User):
    pass
