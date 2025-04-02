from .base_expression import BaseExpression


class BlinkExpression(BaseExpression):
    def __init__(self):
        super().__init__()
        self.upper_lid_left = 159
        self.lower_lid_left = 145
        self.upper_lid_right = 386
        self.lower_lid_right = 374

        self.eye_corner_left = (33, 133)
        self.eye_corner_right = (362, 263)

        # Independent eye state
        self.left_baseline = None
        self.right_baseline = None

        self.left_frame_buffer = 0
        self.right_frame_buffer = 0

        self.left_cooldown = 0
        self.right_cooldown = 0

        self.left_past_state = "open"
        self.right_past_state = "open"

        self.required_frames = 3
        self.cooldown_frames = 8

        self.blink_count = 0

    def set_baseline(self, landmarks):
        left_gap = self.get_distance(landmarks[self.upper_lid_left], landmarks[self.lower_lid_left])
        left_width = self.get_distance(landmarks[self.eye_corner_left[0]], landmarks[self.eye_corner_left[1]])
        right_gap = self.get_distance(landmarks[self.upper_lid_right], landmarks[self.lower_lid_right])
        right_width = self.get_distance(landmarks[self.eye_corner_right[0]], landmarks[self.eye_corner_right[1]])

        self.left_baseline = left_gap / left_width
        self.right_baseline = right_gap / right_width

    def update(self, landmarks):
        if self.left_baseline is None or self.right_baseline is None:
            return None

        # LEFT EYE
        left_gap = self.get_distance(landmarks[self.upper_lid_left], landmarks[self.lower_lid_left])
        left_width = self.get_distance(landmarks[self.eye_corner_left[0]], landmarks[self.eye_corner_left[1]])
        norm_left = left_gap / left_width
        left_threshold = self.left_baseline * 0.45

        if norm_left < left_threshold:
            self.left_frame_buffer += 1
            if self.left_frame_buffer >= self.required_frames and self.left_past_state == "open" and self.left_cooldown == 0:
                self.blink_count += 1
                print(f"Blink (Left) #{self.blink_count}")
                self.left_past_state = "closed"
                self.left_cooldown = self.cooldown_frames
        else:
            self.left_frame_buffer = 0
            if self.left_past_state == "closed":
                self.left_past_state = "open"

        if self.left_cooldown > 0:
            self.left_cooldown -= 1

        # --- RIGHT EYE ---
        right_gap = self.get_distance(landmarks[self.upper_lid_right], landmarks[self.lower_lid_right])
        right_width = self.get_distance(landmarks[self.eye_corner_right[0]], landmarks[self.eye_corner_right[1]])
        norm_right = right_gap / right_width
        right_threshold = self.right_baseline * 0.45

        if norm_right < right_threshold:
            self.right_frame_buffer += 1
            if self.right_frame_buffer >= self.required_frames and self.right_past_state == "open" and self.right_cooldown == 0:
                self.blink_count += 1
                print(f"Blink (Right) #{self.blink_count}")
                self.right_past_state = "closed"
                self.right_cooldown = self.cooldown_frames
        else:
            self.right_frame_buffer = 0
            if self.right_past_state == "closed":
                self.right_past_state = "open"

        if self.right_cooldown > 0:
            self.right_cooldown -= 1

        return {
            "left_eye": self.left_past_state,
            "right_eye": self.right_past_state
        }
