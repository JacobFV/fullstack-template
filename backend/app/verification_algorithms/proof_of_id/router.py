from fastapi import APIRouter

from app.verification_algorithms.proof_of_id.schema import crud_router

router = APIRouter()
router.include_router(crud_router)
