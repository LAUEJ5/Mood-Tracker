from .base_expression import BaseExpression

class SmileExpression(BaseExpression):
    def __init__(self):
        super().__init__()
        self.left_mouth = 78
        self.right_mouth = 308
        self.left_eye = 263
        self.right_eye = 33
        self.upper_lip_index = 13
        self.lower_lip_index = 14
        self.baseline_left = None
        self.baseline_right = None
        self.past_state = "neutral"
        self.smile_count = 0
        self.open_smile_count = 0
        self.closed_smile_count = 0

    def set_baseline(self, landmarks):
        eye_dist = self.get_distance(landmarks[33], landmarks[263])
        self.baseline_left = self.get_distance(landmarks[self.left_mouth], landmarks[self.left_eye]) / eye_dist
        self.baseline_right = self.get_distance(landmarks[self.right_mouth], landmarks[self.right_eye]) / eye_dist

    def update(self, landmarks):
        if self.baseline_left is None or self.baseline_right is None:
            return None

        eye_dist = self.get_distance(landmarks[33], landmarks[263])
        curr_left = self.get_distance(landmarks[self.left_mouth], landmarks[self.left_eye]) / eye_dist
        curr_right = self.get_distance(landmarks[self.right_mouth], landmarks[self.right_eye]) / eye_dist

        left_threshold = self.baseline_left * 0.98
        right_threshold = self.baseline_right * 0.98

        expression = "neutral"
        if curr_left < left_threshold and curr_right < right_threshold:
            expression = "smile"

        if self.past_state == "neutral" and expression == "smile":
            self.smile_count += 1
            print(f"Smile #{self.smile_count}")

            upper_lip = landmarks[self.upper_lip_index]
            lower_lip = landmarks[self.lower_lip_index]
            lip_gap = self.get_distance(upper_lip, lower_lip) / eye_dist

            if lip_gap > 0.03:
                self.open_smile_count += 1
                print(f"Open-mouth smile #{self.open_smile_count}")
            else:
                self.closed_smile_count += 1
                print(f"Closed-mouth smile #{self.closed_smile_count}")

        self.past_state = expression
        return expression
