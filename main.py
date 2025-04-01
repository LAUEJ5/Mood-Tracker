import cv2
import mediapipe as mp
from expressions.eyebrows import EyebrowExpression

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

eyebrows = EyebrowExpression()

cap = cv2.VideoCapture(0)
baseline_set = False

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

            '''
            h, w, _ = image.shape
            for idx in range(468):
                lm = landmarks[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
                cv2.putText(image, str(idx), (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)'''

            if not baseline_set:
                eyebrows.set_baseline(landmarks)
                baseline_set = True
                print("Baseline set.")
            eyebrows.update(landmarks)

    cv2.imshow('MediaPipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()