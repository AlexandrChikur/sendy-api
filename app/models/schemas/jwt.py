from datetime import datetime

from pydantic import BaseModel


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str


class JWTToken(BaseModel):
    token: str
    meta: JWTMeta
