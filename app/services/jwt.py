from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from pydantic import ValidationError

from app.models.schemas.jwt import JWTMeta, JWTUser
from app.models.schemas.users import User

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 3  # three weeks


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(
    user: User,
    secret_key: str,
    expires_min: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(username=user.username).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=expires_min),
    )


def get_username_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).username
    except jwt.PyJWTError as decode_error:
        raise ValueError("Unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("Malformed payload in token") from validation_error
