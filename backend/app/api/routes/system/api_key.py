from fastapi import APIRouter

from app.schema.system.api_key import crud_router

router = APIRouter()
router.include_router(crud_router)
