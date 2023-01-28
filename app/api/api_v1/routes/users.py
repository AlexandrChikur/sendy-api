from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.models.schemas.users import UserWithToken

router = APIRouter()


@router.get(
    "/me",
    response_model=UserWithToken,
    name="users:get-current-user",
    summary="Get user info",
)
async def retrieve_current_user(
    user: UserWithToken = Depends(get_current_user_authorizer()),
) -> UserWithToken:
    """Returning user info that requests this endpoint by provided token"""
    return user
