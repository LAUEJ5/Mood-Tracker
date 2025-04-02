from .base_expression import BaseExpression

class EyebrowExpression(BaseExpression):
    def __init__(self):
        super().__init__()
        self.left_indices = [52, 55, 65, 107]
        self.right_indices = [285, 295, 282, 336]
        self.left_ref_index = 234
        self.right_ref_index = 454

        self.baseline = None
        self.past_state = "neutral"
        self.raise_count = 0
        self.furrow_count = 0
        self.furrow_frame_buffer = 0
        self.raise_frame_buffer = 0
        self.required_frames = 5
        self.cooldown_frames = 15
        self.cooldown = 0

    def set_baseline(self, landmarks):
        left_brow = self.get_average_landmark(self.left_indices, landmarks)
        right_brow = self.get_average_landmark(self.right_indices, landmarks)
        left_ref = landmarks[self.left_ref_index]
        right_ref = landmarks[self.right_ref_index]

        left_dist = self.get_distance(left_brow, left_ref)
        right_dist = self.get_distance(right_brow, right_ref)

        self.baseline = (left_dist + right_dist) / 2

    def update(self, landmarks):
        if self.baseline is None:
            return None

        left_brow = self.get_average_landmark(self.left_indices, landmarks)
        right_brow = self.get_average_landmark(self.right_indices, landmarks)
        left_ref = landmarks[self.left_ref_index]
        right_ref = landmarks[self.right_ref_index]

        left_dist = self.get_distance(left_brow, left_ref)
        right_dist = self.get_distance(right_brow, right_ref)
        avg_dist = (left_dist + right_dist) / 2

        raise_thresh = self.baseline * 0.04
        furrow_thresh = self.baseline * 0.015

        expression = "neutral"

        if avg_dist > self.baseline + raise_thresh:
            self.raise_frame_buffer += 1
            self.furrow_frame_buffer = 0
            if self.raise_frame_buffer >= self.required_frames:
                expression = "raised"
        elif avg_dist < self.baseline - furrow_thresh:
            self.furrow_frame_buffer += 1
            self.raise_frame_buffer = 0
            if self.furrow_frame_buffer >= self.required_frames:
                expression = "furrowed"
        else:
            self.raise_frame_buffer = 0
            self.furrow_frame_buffer = 0

        if self.past_state == "neutral":
            if expression == "raised":
                self.raise_count += 1
                print(f"Raised count: {self.raise_count}")
            elif expression == "furrowed":
                self.furrow_count += 1
                print(f"Furrowed count: {self.furrow_count}")

        self.past_state = expression
        return expression
