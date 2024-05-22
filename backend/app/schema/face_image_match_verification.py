class FaceImageMatchVerificationBase(VerificationBase):
    algorithm_name: str = "face_image_match_verification-001"


class FaceImageMatchVerification(FaceImageMatchVerificationBase, Verification):
    additional_provided_face_images: list[bytes] | None = None

    @hybrid_property
    def all_provided_face_images(self):
        return self.additional_provided_face_images + [self.who_to_verify.image]

    @all_provided_face_images.expression
    def all_provided_face_images(cls):
        return func.array_cat(
            cls.additional_provided_face_images, func.array([cls.who_to_verify.image])
        )


class FaceImageMatchVerificationPublic(
    FaceImageMatchVerificationBase, VerificationPublic
):
    pass
