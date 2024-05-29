from fastapi import APIRouter

from app.schema.system.api_key_use import crud_router

router = APIRouter()
router.include_router(crud_router)

crud_router = build_crud_endpoints(
    t_model_base=APIKeyUseBase,
    t_model_read=APIKeyUseRead,
    t_model_in_db=APIKeyUse,
)
