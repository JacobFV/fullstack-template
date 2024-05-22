class HumanSpeechVerificationBase(VerificationBase):
    model_name: str = "human_speech_verification-001"


class HumanSpeechVerification(HumanSpeechVerificationBase, Verification):
    pass


class HumanSpeechVerificationPublic(HumanSpeechVerificationBase, VerificationPublic):
    pass
