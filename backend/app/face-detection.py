import cv2
from deepface import DeepFace

# Initialize models
models = ["Facenet"]
DeepFace.stream("database", model_name=models)

def process_latest_frame(
    frames,
    model_name: str,
    send_to_client: callable,
    on_decision: callable,
):
    gray_frame = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY)
    
    # Analyze the latest frame using DeepFace
    result = DeepFace.verify(photos=[gray_frame], database_path="database", model_name=model_name)
    
    # Check if a match was found
    if result["verified"]:
        print("Match found!")
        on_decision(True)  # Send True to indicate a positive decision
    else:
        print("No match found.")
        on_decision(False)  # Send False to indicate a negative decision
    
    return  # Don't return anything because we are streaming this from the client
