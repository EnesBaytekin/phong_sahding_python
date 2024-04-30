from utils import get_distance

class Sphere:
    def __init__(self, x, y, z, radius, color):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
    def get_center(self):
        return [self.x, self.y, self.z]
    def is_colliding_point(self, point):
        return get_distance(point, self.get_center()) <= self.radius
