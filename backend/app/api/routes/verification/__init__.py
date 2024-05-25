from fastapi import APIRouter

from app.api.routes.verification.credit_bureau_verification import (
    router as credit_bureau_verification_router,
)
from app.api.routes.verification.face_video_anomaly_verification import (
    router as face_video_anomaly_verification_router,
)
from app.api.routes.verification.hand_sign_verification import (
    router as hand_sign_verification_router,
)
from app.api.routes.verification.human_speech_verification import (
    router as human_speech_verification_router,
)
from app.api.routes.verification.living_pupil_verification import (
    router as living_pupil_verification_router,
)
from app.api.routes.verification.proof_of_id_verification import (
    router as proof_of_id_verification_router,
)
from app.api.routes.verification.verification import router as verification_router

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
