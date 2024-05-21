import cv2
from deepface import DeepFace

# Initialize models
models = ["VGG-Face"]
DeepFace.stream(db_path="path/to/database", model_name=models[0])

def process_latest_frame(
        frame, 
        model_name: str, 
        send_to_client: callable, 
        on_decision: callable):
    # Convert the frame to grayscale for faster processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = DeepFace.detectFaces(gray_frame)
    
    # Process each detected face
    for face in faces:
        # Extract the face region
        x, y, w, h = face['box']
        face_img = gray_frame[y:y+h, x:x+w]
        
        # Verify the face against the database
        result = DeepFace.verify(photos=[face_img], database_path="path/to/database", model_name=model_name)
        
        # Check if a match was found
        if result["verified"]:
            print(f"Match found for {result['identity']}")
            on_decision(True)  # Send True to indicate a positive decision
        else:
            print("No match found.")
            on_decision(False)  # Send False to indicate a negative decision

# Example usage
cap = cv2.VideoCapture(0)  # Use 0 for the default camera
while True:
    ret, frame = cap.read()
    if not ret:
        break
    process_latest_frame(frame, "Facenet", lambda x: None, lambda x: None)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
