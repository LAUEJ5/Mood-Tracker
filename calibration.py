import cv2
import mediapipe as mp
import numpy as np

class Calibrator:
    def __init__(self, expressions):
        self.expressions = expressions
        self.face_mesh = mp.solutions.face_mesh.FaceMesh()
        self.drawing_utils = mp.solutions.drawing_utils
        self.calibrated = False

    def overlay_head_guide(self, frame):
        h, w, _ = frame.shape
        center = (w // 2, h // 2 - 100)

        # Draw head as ellipse (2x taller, 1.5x wider)
        head_width = 150  # base width
        head_height = 220  # base height (was 110 before)
        head_axes = (int(head_width * 1.25), int(head_height * 1.12))  # 1.5x wider, 2x taller
        cv2.ellipse(frame, center, head_axes, 0, 0, 360, (0, 255, 0), 2)

        # Draw downward-curving shoulders at bottom
        shoulder_center = (w // 2, h - 60)
        shoulder_axes = (300, 100)
        cv2.ellipse(frame, shoulder_center, shoulder_axes, 0, 180, 360, (0, 255, 0), 2)

        cv2.putText(frame, "Align your face here", (center[0] - 160, center[1] - 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Press ENTER to calibrate", (shoulder_center[0] - 180, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


    def run(self, cap):
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.drawing_utils.draw_landmarks(
                        frame, face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)

                    landmarks = face_landmarks.landmark

                    self.overlay_head_guide(frame)
                    cv2.imshow('Calibration', frame)

                    key = cv2.waitKey(1)
                    if key == 13:  # ENTER key
                        for exp in self.expressions:
                            exp.set_baseline(landmarks)
                        self.calibrated = True
                        print("Calibration complete!")
                        return True

            else:
                self.overlay_head_guide(frame)
                cv2.imshow('Calibration', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        return False
