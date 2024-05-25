from fastapi import APIRouter

from app.api.routes import router as api_router
from app.api.routes import login
from app.api.routes import users
from app.api.routes import utils

# leave this here from the origonal template
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
