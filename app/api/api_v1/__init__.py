from app.core.utils import VersionedAPIRouter

from .routes import users

router = VersionedAPIRouter(1, 0)
router.include_router(users.router, tags=["users"], prefix="/users")
