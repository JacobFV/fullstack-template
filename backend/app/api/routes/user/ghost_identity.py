from fastapi import APIRouter

from app.schema.user.ghost_identity import crud_router

router = APIRouter()
router.include_router(crud_router)
crud_router = build_crud_endpoints(
    t_model_base=GhostIdentityBase,
    t_model_create=GhostIdentityCreate,
    t_model_read=GhostIdentityRead,
    t_model_update=GhostIdentityUpdate,
    t_model_in_db=GhostIdentity,
)
