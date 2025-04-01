import mediapipe as mp
from math import sqrt

class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.mp_drawing = mp.solutions.drawing_utils
        self.eyebrow_distance = None
        self.furrow_count = 0
        self.raise_count = 0
        self.past_eyebrow = "neutral"


    def get_distance(self, point1, point2):
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z

        return sqrt(dx**2 + dy**2 + dz**2)

    
    def set_baseline(self, landmarks):
        ref = landmarks[168]
        eye_distance = self.get_distance(landmarks[33], landmarks[263])
        self.eyebrow_distance = self.get_distance(landmarks[107], ref) / eye_distance


    def update_eyebrow_state(self, landmarks):
        if self.eyebrow_distance is None:
            return

        current_eye_distance = self.get_distance(landmarks[33], landmarks[263])
        normalized_eyebrow_dist = self.get_distance(landmarks[107], landmarks[168]) / current_eye_distance
        raise_threshold = 0.02
        furrow_threshold = 0.01
        expression = "neutral"
        if normalized_eyebrow_dist > self.eyebrow_distance + raise_threshold:
            expression = "raised"
        elif normalized_eyebrow_dist < self.eyebrow_distance - furrow_threshold:
            expression = "furrowed"

        if self.past_eyebrow == "neutral" and expression == "raised":
            self.raise_count += 1
            print(f"Raise count: {self.raise_count}")
        elif self.past_eyebrow == "neutral" and expression == "furrowed":
            self.furrow_count += 1
            print(f"Furrow count: {self.furrow_count}")
        self.past_eyebrow = expression
