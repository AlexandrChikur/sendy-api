from pydantic import EmailStr
from pydantic.class_validators import validator

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.schemas.rwschema import RWSchema
from app.services import security


class User(RWModel, DateTimeModelMixin):
    username: str
    email: str


class UserInLogin(RWSchema):
    email: EmailStr
    password: str

    @validator("password")
    def check_password_strength(cls, pwd: str) -> str:
        if len(pwd) < 6:
            raise ValueError("Length should be at least 6")
        if not any(char.isdigit() for char in pwd):
            raise ValueError("Password should have at least one numeral")
        if not any(char.isupper() for char in pwd):
            raise ValueError("Password should have at least one uppercase letter")
        return pwd


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


class UserWithToken(User, IDModelMixin):
    token: str


class UserInResponse(RWSchema, User, IDModelMixin):
    pass


class UserInDB(IDModelMixin, User):
    salt: str = ""
    hashed_password: str = ""
    is_active: bool = False

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)
