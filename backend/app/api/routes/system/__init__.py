from fastapi import APIRouter

from app.api.routes.system.api_key import router as api_key_router
from app.api.routes.system.api_key_use import router as api_key_use_router

router = APIRouter()
router.include_router(api_key_router, prefix="/api-key")
router.include_router(api_key_use_router, prefix="/api-key-use")
