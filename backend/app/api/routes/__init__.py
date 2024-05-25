from fastapi import APIRouter

from app.api.routes.system import router as system_router
from app.api.routes.user import router as user_router
from app.api.routes.verification import router as verification_router

router = APIRouter()
router.include_router(system_router, tags=["system"])
router.include_router(user_router, tags=["user"])
router.include_router(verification_router, tags=["verification"])
