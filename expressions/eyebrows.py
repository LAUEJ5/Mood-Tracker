from .base_expression import BaseExpression

class EyebrowExpression(BaseExpression):
    def __init__(self):
        super().__init__()
        self.indices = [52, 53, 55, 65, 107]
        self.baseline = None
        self.past_state = "neutral"
        self.count = 0

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

        raise_thresh = 0.02
        furrow_thresh = 0.01

        expression = "neutral"
        if norm_dist > self.baseline + raise_thresh:
            expression = "raised"
        elif norm_dist < self.baseline - furrow_thresh:
            expression = "furrowed"

        if self.past_state == "neutral" and expression != "neutral":
            self.count += 1
            print(f"{expression.capitalize()} count: {self.count}")
        
        self.past_state = expression
        return expression
