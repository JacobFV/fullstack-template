from fastapi import APIRouter

from app.schema.verification.face_video_anomaly_verification import crud_router

router = APIRouter()
router.include_router(crud_router)
