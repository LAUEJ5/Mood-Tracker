import cv2
import mediapipe as mp
from expressions.eyebrows import EyebrowExpression
from expressions.smile import SmileExpression
from expressions.eyes import BlinkExpression

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

eyebrows = EyebrowExpression()
smile = SmileExpression()
blink = BlinkExpression()

cap = cv2.VideoCapture(0)
calibrated = False
tracking = False
print("Relax your face completely and get close to the camera.")
print("Press ENTER to calibrate.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            mp_drawing.draw_landmarks(
                image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION
            )

            '''list = [234, 454]
            h, w, _ = image.shape
            for idx in list:
                lm = landmarks[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
                cv2.putText(image, str(idx), (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)'''

            if not calibrated:
                cv2.imshow('Facial Tracker', image)
                if cv2.waitKey(1) & 0xFF == 13:
                    eyebrows.set_baseline(landmarks)
                    smile.set_baseline(landmarks)
                    blink.set_baseline(landmarks)
                    calibrated = True
                    print("Calibration complete! Press ENTER again to start tracking.")
                continue

            if calibrated and not tracking:
                cv2.imshow('Facial Tracker', image)
                if cv2.waitKey(1) & 0xFF == 13:
                    tracking = True
                    print("Tracking started. Facial expression counts active.")
                continue

            if tracking:
                blink.update(landmarks)
                smile_state = smile.update(landmarks)
                if smile_state != "smile":
                    eyebrows.update(landmarks)


    cv2.imshow('Facial Tracker', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()