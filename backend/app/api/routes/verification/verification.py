from fastapi import APIRouter

from app.schema.verification.verification import crud_router

router = APIRouter()
router.include_router(crud_router)
