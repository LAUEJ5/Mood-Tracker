class BaseExpression:
    def __init__(self):
        self.eye_indices = (33, 263)
        self.ref_index = 168

    def get_distance(self, point1, point2):
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        dz = point1.z - point2.z
        return (dx**2 + dy**2 + dz**2) ** 0.5

    def get_average_landmark(self, indices, landmarks):
        x = sum(landmarks[i].x for i in indices) / len(indices)
        y = sum(landmarks[i].y for i in indices) / len(indices)
        z = sum(landmarks[i].z for i in indices) / len(indices)
        class Point: pass
        point = Point()
        point.x, point.y, point.z = x, y, z
        return point