from fastapi import APIRouter

from app.schema.user.identity import crud_router

router = APIRouter()
router.include_router(crud_router)
