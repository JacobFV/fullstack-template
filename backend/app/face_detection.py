import face_recognition
import cv2
import aio_pika
import numpy as np

from app.schema import VerificationRequest


class FaceRecognitionHandler:
    def __init__(self, verification_request: VerificationRequest):
        self.video_capture = None
        self.face_locations = []
        self.frame_count = 0  # Initialize frame count
        self.verification_request = verification_request
        # hook up the handler for new amqp messages
        self.verification_request.amqp_queue().consume(self.handle_message)

    async def consumer(message: aio_pika.IncomingMessage):
        # This is where you process JSON that the client sends to you
        # IDK what you will do here
        text = message.body()
        print(text)

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

        self.frame_count += 1  # Increment the frame count
        return True

    def start_processing(self, video_source=0):
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            print("Cannot open video source")
            exit()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting...")
                break
            if not self.process_frame(frame):
                break
        cap.release()


# Example usage
handler = FaceRecognitionHandler()
# handler.start_processing()
