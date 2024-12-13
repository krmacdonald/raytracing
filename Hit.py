
from Vector3 import Vector3
from Point3 import Point3

class Hit:
    def __init__(self):
        self.t = -1  # No hit by default
        self.norm = Vector3()
        self.point = Point3()
        self.obj = None
