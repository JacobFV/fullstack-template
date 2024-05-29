from fastapi import APIRouter

from app.verification_algorithms.credit_bureau.schema import (
    crud_router,
)

router = APIRouter()
router.include_router(crud_router)
