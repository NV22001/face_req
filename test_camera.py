import cv2

cap = cv2.VideoCapture(2)  # Try index 1, 2, or higher

if not cap.isOpened():
    print("Cannot access the camera")
else:
    print("Camera is accessible")
    cap.release()