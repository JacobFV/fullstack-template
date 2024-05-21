import face_recognition
import cv2

class FaceRecognitionHandler:
    def __init__(self):
        self.video_capture = None
        self.face_locations = []

    def initialize_video(self):
        # Get a reference to webcam #0 (the default one)
        self.video_capture = cv2.VideoCapture(0)

    def release_video(self):
        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()

    def process_frame(self):
        # Grab a single frame of video
        ret, frame = self.video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if len(self.face_locations) > 0:
            # Find all the faces and face locations in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_locations = [y * 4 for y in self.face_locations]  # Scale up the coordinates back to the original frame size

        # Draw a box around the faces
        for (top, right, bottom, left) in self.face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False

        return True

    def start_processing(self):
        while True:
            if not self.process_frame():
                break

# Example usage
handler = FaceRecognitionHandler()
handler.initialize_video()
handler.start_processing()
