from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.models.schemas.users import User, UserInResponse

router = APIRouter()


@router.get("/me", response_model=UserInResponse, name="users:get-current-user")
async def retrieve_current_user(
    user: User = Depends(get_current_user_authorizer()),
) -> UserInResponse:
    return UserInResponse(**user.dict())
