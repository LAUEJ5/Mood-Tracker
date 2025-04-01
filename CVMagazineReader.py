import cv2
import mediapipe as mp
from FaceAnalyzer import FaceAnalyzer

analyzer = FaceAnalyzer()
cap = cv2.VideoCapture(0)

baseline_set = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = analyzer.face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            analyzer.mp_drawing.draw_landmarks(
                image, face_landmarks, analyzer.mp_face_mesh.FACEMESH_TESSELATION
            )
            important_indices = list(range(468))
            h, w, _ = image.shape

            for idx in important_indices:
                lm = face_landmarks.landmark[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (x, y), 4, (0, 255, 0), -1)
                cv2.putText(image, str(idx), (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


            if not baseline_set:
                analyzer.set_baseline(landmarks)
                baseline_set = True
                print("Baseline set.")

            analyzer.update_eyebrow_state(landmarks)

    cv2.imshow('MediaPipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()