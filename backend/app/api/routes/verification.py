from fastapi import APIRouter

from app.verification.credit_bureau.router import (
    router as credit_bureau_verification_router,
)
from app.verification.face_video_anomaly_verification.router import (
    router as face_video_anomaly_verification_router,
)
from app.verification.hand_sign_verification.router import (
    router as hand_sign_verification_router,
)
from app.verification.human_speech_verification.router import (
    router as human_speech_verification_router,
)
from app.verification.living_pupil_verification.router import (
    router as living_pupil_verification_router,
)
from app.verification.proof_of_id_verification.router import (
    router as proof_of_id_verification_router,
)
from app.verification.verification.router import router as verification_router

router = APIRouter()
router.include_router(credit_bureau_verification_router, prefix="/credit-bureau")
router.include_router(
    face_video_anomaly_verification_router, prefix="/face-video-anomaly"
)
router.include_router(hand_sign_verification_router, prefix="/hand-sign")
router.include_router(human_speech_verification_router, prefix="/human-speech")
router.include_router(living_pupil_verification_router, prefix="/living-pupil")
router.include_router(proof_of_id_verification_router, prefix="/proof-of-id")
router.include_router(verification_router)
