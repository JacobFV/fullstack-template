from fastapi import APIRouter

from app.schema.verification.credit_bureau_verification import crud_router

router = APIRouter()
router.include_router(crud_router)
