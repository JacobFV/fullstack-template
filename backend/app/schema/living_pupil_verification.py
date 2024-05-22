class LivingPupilVerificationBase(VerificationBase):
    model_name: str = "living_pupil_verification-001"


class LivingPupilVerification(LivingPupilVerificationBase, Verification):
    pass


class LivingPupilVerificationPublic(LivingPupilVerificationBase, VerificationPublic):
    pass
