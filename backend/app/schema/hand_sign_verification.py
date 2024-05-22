class HandSignVerificationBase(VerificationBase):
    model_name: str = "hand_sign_verification-001"


class HandSignVerification(HandSignVerificationBase, Verification):
    hand_letters: list[str]


class HandSignVerificationPublic(HandSignVerificationBase, VerificationPublic):
    pass
