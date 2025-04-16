import threading
import cv2
from deepface import DeepFace
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

reference_img = cv2.imread("test.jpg")  # Reference image
face_match = False

def check_face(frame):
    """Verify if the face in the frame matches the reference image."""
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream video frames to the frontend."""
    def generate_frames():
        global face_match
        counter = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if counter % 30 == 0:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            counter += 1

            # Add match status text to the frame
            if face_match:
                cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Close the video feed and release resources."""
    global cap
    cap.release()
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(debug=True)