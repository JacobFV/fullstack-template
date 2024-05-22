class CreditBureauVerificationBase(VerificationBase):
    pass


class CreditBureauVerification(CreditBureauVerificationBase, Verification):
    pass


class CreditBureauVerificationPublic(CreditBureauVerificationBase, VerificationPublic):
    pass
