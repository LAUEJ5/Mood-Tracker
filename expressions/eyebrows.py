from .base_expression import BaseExpression

class EyebrowExpression(BaseExpression):
    def __init__(self):
        super().__init__()
        self.indices = [52, 53, 55, 65, 107]
        self.baseline = None
        self.past_state = "neutral"
        self.raise_count = 0
        self.furrow_count = 0

        # Redundancy controls
        self.furrow_frame_buffer = 0
        self.raise_frame_buffer = 0
        self.required_frames = 5  # frames needed to confirm expression
        self.cooldown_frames = 15
        self.cooldown = 0

    def set_baseline(self, landmarks):
        eyebrow_avg = self.get_average_landmark(self.indices, landmarks)
        eye_dist = self.get_distance(landmarks[self.eye_indices[0]], landmarks[self.eye_indices[1]])
        ref = landmarks[self.ref_index]
        self.baseline = self.get_distance(eyebrow_avg, ref) / eye_dist

    def update(self, landmarks):
        if self.baseline is None:
            return None

        eyebrow_avg = self.get_average_landmark(self.indices, landmarks)
        eye_dist = self.get_distance(landmarks[self.eye_indices[0]], landmarks[self.eye_indices[1]])
        ref = landmarks[self.ref_index]
        norm_dist = self.get_distance(eyebrow_avg, ref) / eye_dist

        raise_thresh = self.baseline * 0.10
        furrow_thresh = self.baseline * 0.015

        expression = "neutral"

        # Detect raised
        if norm_dist > self.baseline + raise_thresh:
            self.raise_frame_buffer += 1
            self.furrow_frame_buffer = 0
            if self.raise_frame_buffer >= self.required_frames:
                expression = "raised"
        # Detect furrowed
        elif norm_dist < self.baseline - furrow_thresh:
            self.furrow_frame_buffer += 1
            self.raise_frame_buffer = 0
            if self.furrow_frame_buffer >= self.required_frames:
                expression = "furrowed"
        else:
            self.furrow_frame_buffer = 0
            self.raise_frame_buffer = 0

        # Count only on transition from neutral
        if self.past_state == "neutral":
            if expression == "furrowed":
                self.furrow_count += 1
                print(f"Furrowed count: {self.furrow_count}")
            elif expression == "raised":
                self.raise_count += 1
                print(f"Raised count: {self.raise_count}")

        self.past_state = expression
        return expression
