from fastapi import APIRouter

from app.schema.verification.proof_of_id_verification import crud_router

router = APIRouter()
router.include_router(crud_router)
