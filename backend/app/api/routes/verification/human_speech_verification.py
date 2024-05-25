from fastapi import APIRouter

from app.schema.verification.human_speech_verification import crud_router

router = APIRouter()
router.include_router(crud_router)
