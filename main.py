import cv2
import mediapipe as mp
from expressions.eyebrows import EyebrowExpression
from expressions.smile import SmileExpression
from expressions.eyes import BlinkExpression
from calibration import Calibrator


eyebrows = EyebrowExpression()
smile = SmileExpression()
blink = BlinkExpression()
expressions = [eyebrows, smile, blink]
cap = cv2.VideoCapture(0)

# Run calibration step
calibrator = Calibrator(expressions)
success = calibrator.run(cap)

if not success:
    print("Calibration aborted.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

print("Calibration complete. Press ENTER to begin tracking.")

# Wait for ENTER key to begin tracking
while True:
    if cv2.waitKey(1) & 0xFF == 13:
        print("Tracking started.")
        break

# Main tracking loop
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # Draw mesh
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION
            )

            # Update expressions
            eyebrows.update(landmarks)
            smile.update(landmarks)
            blink.update(landmarks)

    cv2.imshow('Facial Tracker', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
