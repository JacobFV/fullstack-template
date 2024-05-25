from fastapi import APIRouter

from app.schema.user.user import crud_router

router = APIRouter()
router.include_router(crud_router)
