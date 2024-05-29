from fastapi import APIRouter

from app.schema.user.identity import crud_router

router = APIRouter()
router.include_router(crud_router)

crud_router = build_crud_endpoints(
    t_model_base=IdentityBase,
    t_model_create=IdentityCreate,
    t_model_read=IdentityRead,
    t_model_update=IdentityUpdate,
    t_model_in_db=Identity,
)
