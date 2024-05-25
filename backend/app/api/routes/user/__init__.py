from fastapi import APIRouter

from app.api.routes.user.developer import router as developer_router
from app.api.routes.user.ghost_identity import router as ghost_identity_router
from app.api.routes.user.identity import router as identity_router
from app.api.routes.user.user import router as user_router

router = APIRouter()
router.include_router(developer_router, prefix="/developer")
router.include_router(ghost_identity_router, prefix="/ghost-identity")
router.include_router(identity_router, prefix="/identity")
router.include_router(user_router, prefix="/user")
