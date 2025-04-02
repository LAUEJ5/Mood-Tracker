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

        self.smile_active = False
        self.smile_was_open = False
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

        smile_now = curr_left < left_threshold and curr_right < right_threshold

        upper_lip = landmarks[self.upper_lip_index]
        lower_lip = landmarks[self.lower_lip_index]
        lip_gap = self.get_distance(upper_lip, lower_lip) / eye_dist

        open_now = lip_gap > 0.03

        # Smile Start
        if smile_now and not self.smile_active:
            self.smile_active = True
            self.smile_was_open = open_now 

        # Smile Ongoing 
        elif smile_now and self.smile_active:
            self.smile_was_open = self.smile_was_open or open_now

        # Smile End
        elif not smile_now and self.smile_active:
            self.smile_active = False
            self.smile_count += 1
            print(f"Smile #{self.smile_count}")
            if self.smile_was_open:
                self.open_smile_count += 1
                print(f"Open-mouth smile #{self.open_smile_count}")
            else:
                self.closed_smile_count += 1
                print(f"Closed-mouth smile #{self.closed_smile_count}")

        return "smile" if smile_now else "neutral"
