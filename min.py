import cv2

cap = cv2.VideoCapture(0)  # Open the default camera

if not cap.isOpened():
    print("Cannot access the camera")
else:
    print("Camera is accessible")
    cap.release()