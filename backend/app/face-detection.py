from deepface import DeepFace
import cv2


models = ["VGG-Face", "Facenet", "OpenFace", "DeepID", "ArcFace", "Dlib", "SFace"]

DeepFace.stream('database', model_name="models")
