from datetime import datetime
import face_recognition
import cv2
import aio_pika

from app.schema import (
    OneTimeVerifiableIdentity,
    UserThatRequestsVerification,
    Verification,
)


class FaceRecognitionHandler:
    def __init__(self, verification_request: Verification):
        self.video_capture = None
        self.face_locations = []
        self.frame_count = 0  # Initialize frame count
        self.verification_request = verification_request
        # hook up the handler for new amqp messages
        self.verification_request.listen_for_messages(self.consumer)

    async def consumer(self, data: str):
        print(data)

    def process_frame(self, frame):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.frame_count % 2 == 0:  # Check if the frame count is even
            # Find all the faces and face locations in the current frame of video
            new_face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_locations.extend(
                new_face_locations
            )  # Append new detections to existing locations

        # Draw a box around the faces
        for top, right, bottom, left in self.face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        self.verification_request.publish_message("we're processing the frame")

        # Let's suppose you detected a face
        if True:  # say, you detected a face
            # send a message to the queue
            self.verification_request.publish_message("face detected")

        self.frame_count += 1  # Increment the frame count
        return True


def test_local_face_detection():
    handler = FaceRecognitionHandler(
        verification_request=Verification(
            id=1,
            who_to_verify=OneTimeVerifiableIdentity(id=1, image=b""),
            on_completion_redirect_url="",
            on_completion_webhook_url="",
            verification_requested_by=UserThatRequestsVerification(
                id=2,
                name="Test Developer",
                image=b"",
                email="test@example.com",
                is_verified=True,
                is_active=True,
                full_name="Test Developer",
                hashed_password="",
                is_superuser=True,
                stripe_user_access_token="",
            ),
            verification_requested_at=datetime.now(),
            verification_requested_by_id=2,
            check_anomaly_in_face_video=False,
            ask_to_make_hand_signs=False,
            hand_letters=None,
            check_match_against_provided_face_images=False,
            additional_provided_face_images=[],
            check_fingerprint=False,
        )
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open video source")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break
        face = handler.process_frame(frame)
        if not face:
            break
    cap.release()


if __name__ == "__main__":
    test_loacl_face_detection()
