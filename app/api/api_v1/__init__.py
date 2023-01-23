from fastapi.routing import APIRouter

from .routes import authentication, messages, users

router = APIRouter()
router.include_router(authentication.router, tags=["Authentication"], prefix="/auth")
router.include_router(users.router, tags=["Users"], prefix="/users")
router.include_router(messages.router, tags=["Messages"], prefix="/messages")
