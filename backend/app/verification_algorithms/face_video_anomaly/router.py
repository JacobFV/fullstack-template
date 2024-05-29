from fastapi import APIRouter

from app.verification_algorithms.face_video_anomaly.schema import (
    crud_router,
)

router = APIRouter()
router.include_router(crud_router)
