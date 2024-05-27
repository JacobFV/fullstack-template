from fastapi import APIRouter
from app.schema.system.api_key import crud_router
from app.schema.user.developer import Developer
from app.schema.base import ModelInDB
from app.schema.system.api_key import APIKeyBase

from app.schema.system.api_key import APIKey, APIKeyRead

class APIKey(APIKeyBase, ModelInDB):
    owner: Developer

router = APIRouter()
router.include_router(crud_router)
