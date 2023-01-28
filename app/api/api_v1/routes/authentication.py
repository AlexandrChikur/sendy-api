import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInCreate, UserInLogin, UserWithToken
from app.resources import strings
from app.services import jwt
from app.services.authentication import (check_email_is_taken,
                                         check_username_is_taken)

router = APIRouter()
settings = get_app_settings()


@router.post(
    "/signup",
    response_model=UserWithToken,
    name="auth:create-user",
    summary="Create user (Sign Up)",
    tags=["Internal"],
    include_in_schema=settings.debug,
)
async def register(
    user_create: UserInCreate = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserWithToken:
    """Sign up user interface"""
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user = await users_repo.create_user(**user_create.dict())

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return UserWithToken(
        id=user.id,
        username=user.username,
        email=user.email,
        token=token,
    )


@router.post(
    "/token",
    response_model=UserWithToken,
    name="auth:token",
    summary="Get user token for authentication",
)
async def login(
    user_login: UserInLogin = Body(...),
    token_exp_minutes: int = Query(
        None,
        alias="expires_minutes",
        ge=5,
        le=129600,  # 3 months
        description="Token will expire after provided minutes if it's provided",
    ),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserWithToken:
    """ Get user's JWT token authentication interface.\n
        Creation token with your own expiration value is able only in range from 5 min to 129600 (3 months)
        Default token expired in: **3 weeks**
    """
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await users_repo.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    if token_exp_minutes:
        token = jwt.create_access_token_for_user(
            user,
            str(settings.secret_key.get_secret_value()),
            expires_td=datetime.timedelta(minutes=token_exp_minutes),
        )
    else:
        token = jwt.create_access_token_for_user(
            user,
            str(settings.secret_key.get_secret_value()),
        )

    return UserWithToken(
        id=user.id,
        username=user.username,
        email=user.email,
        token=token,
    )
