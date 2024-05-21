import cv2
from deepface import DeepFace


models = ["VGG-Face", "Facenet", "OpenFace", "DeepID", "ArcFace", "Dlib", "SFace"]

DeepFace.stream('database', model_name="models")


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray_frame = cv2.cvtColor(frame)


cap.release()
cv2.destroyAllWindows()