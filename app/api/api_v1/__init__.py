from fastapi.routing import APIRouter

from .routes import authentication, users

router = APIRouter()
router.include_router(authentication.router, tags=["Authentication"], prefix="/auth")
router.include_router(users.router, tags=["Users"], prefix="/users")
