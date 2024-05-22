class FaceVideoAnomalyVerificationBase(VerificationBase):
    model_name: str = "face_video_anomaly_verification-001"


class FaceVideoAnomalyVerificationRequest(
    FaceVideoAnomalyVerificationBase, VerificationRequestBase
):
    pass


class FaceVideoAnomalyVerification(Verification):
    pass


class FaceVideoAnomalyVerificationPublic(
    FaceVideoAnomalyVerificationBase, VerificationPublic
):
    pass
