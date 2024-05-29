from fastapi import APIRouter
from app.schema.system.api_key import crud_router
from app.schema.user.developer import Developer
from app.schema.base import ModelInDB
from app.schema.system.api_key import APIKeyBase

# originally had an underscore on the second argument
from app.schema.system.api_key import APIKey as APIKey, APIKeyRead as APIKeyRead

# from app.schema.system.api_key import APIKey, APIKeyRead

router = APIRouter()
router.include_router(crud_router)
crud_router = build_crud_endpoints(
    t_model_base=APIKeyBase,
    t_model_create=APIKeyCreate,
    t_model_read=APIKeyRead,
    t_model_update=APIKeyUpdate,
    t_model_in_db=APIKey,
)
