from fastapi.routing import APIRouter

from app.api import api_v1

router = APIRouter()
router.include_router(api_v1.router, tags=["v1"], prefix="/v1")
