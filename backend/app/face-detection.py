from deepface import DeepFace


models = ["VGG-Face", "Facenet", "OpenFace", "DeepID", "ArcFace", "Dlib", "SFace"]

DeepFace.stream("database", model_name="models")


def process_latest_frame(
    frames,
    model_name: str,
    send_to_client: callable,
    on_decision: callable,
):
    gray_frame = cv2.cvtColor(frames[:-1])
    # do your logic
    if (
        False
    ):  # if you determine that sufficient evidence has accumulated to make a decision
        on_decision(True)  # or False
    return  # don't return anything because we are streaming this from the client
