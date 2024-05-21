import cv2
from deepface import DeepFace


models = ["Facenet"]

DeepFace.stream('database', model_name="models")


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2GRAY)

    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, ym, w, h) in faces:
        face_roi = rgb_frame[y:y + h, x:x + w]




cap.release()
cv2.destroyAllWindows()