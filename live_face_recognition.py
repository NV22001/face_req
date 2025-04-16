import os
import cv2
from deepface import DeepFace
import threading

# Disable GPU usage and suppress TensorFlow logs
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Force TensorFlow to use CPU
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress TensorFlow logs (1=INFO, 2=WARNING, 3=ERROR)

# Initialize the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the reference image for face matching
reference_img = cv2.imread("test.jpg")  # Replace this with your reference image
face_match = False  # Global variable to store the matching result


def check_face(frame):
    """
    Function to check whether the face in the given frame matches the reference image.
    Runs in a separate thread to prevent blocking.
    """
    global face_match
    try:
        # Perform face verification using DeepFace
        result = DeepFace.verify(frame, reference_img.copy())
        face_match = result['verified']
    except Exception as e:
        print(f"Error in face recognition: {e}")
        face_match = False


# Open the video capture (camera)
cap = cv2.VideoCapture(0)  # Use 0 for the default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height

# Check if the camera is accessible
if not cap.isOpened():
    print("Cannot access the camera. Make sure it is connected and not used by another application.")
    exit()

counter = 0  # Counter to limit the frequency of face verification

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if ret:
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Perform face recognition every 30 frames
        if counter % 30 == 0 and len(faces) > 0:  # Only if faces are detected
            threading.Thread(target=check_face, args=(frame.copy(),)).start()

        # Increase the frame counter
        counter += 1

        # Display the result of face recognition
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # Show the video feed
        cv2.imshow('Live Face Recognition', frame)

    # Exit the loop when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()