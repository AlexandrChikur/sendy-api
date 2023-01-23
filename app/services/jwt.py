from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from app.models.schemas.jwt import JWTMeta, JWTToken, JWTUser
from app.models.schemas.users import User

JWT_ACCESS_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TD = timedelta(weeks=3)  # three weeks


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    subject: str,
    secret_key: str,
    expires_td: timedelta,
) -> JWTToken:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_td
    jwt_meta = JWTMeta(exp=expire, sub=subject)
    to_encode.update(jwt_meta.dict())
    return JWTToken(
        token=jwt.encode(to_encode, secret_key, algorithm=ALGORITHM), meta=jwt_meta
    )


def create_access_token_for_user(
    user: User,
    secret_key: str,
    expires_td: timedelta = ACCESS_TOKEN_EXPIRE_TD,
) -> JWTToken:
    return create_jwt_token(
        jwt_content=JWTUser(username=user.username).dict(),
        subject=JWT_ACCESS_SUBJECT,
        secret_key=secret_key,
        expires_td=expires_td,
    )


def get_username_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).username
    except jwt.PyJWTError as decode_error:
        raise ValueError("Unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("Malformed payload in token") from validation_error
