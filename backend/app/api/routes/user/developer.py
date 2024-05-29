from fastapi import APIRouter

from app.schema.user.developer import crud_router

router = APIRouter()
router.include_router(crud_router)
crud_router = build_crud_endpoints(
    t_model_base=DeveloperBase,
    t_model_create=DeveloperCreate,
    t_model_read=DeveloperRead,
    t_model_update=DeveloperUpdate,
    t_model_in_db=Developer,
)
