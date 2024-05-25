from fastapi import APIRouter

from app.schema.verification.hand_sign_verification import crud_router

router = APIRouter()
router.include_router(crud_router)
