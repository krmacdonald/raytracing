
import math

class Vector3:
    def __init__(self, dx=0.0, dy=0.0, dz=0.0):
        self.dx = dx
        self.dy = dy
        self.dz = dz

    @classmethod
    def from_points(cls, p1, p2=None):
        if p2 is None:
            return cls(p1.x, p1.y, p1.z)
        return cls(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

    def magnitude(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            self.dx /= mag
            self.dy /= mag
            self.dz /= mag

    def dot(self, other):
        return self.dx * other.dx + self.dy * other.dy + self.dz * other.dz

    def cross(self, other):
        return Vector3(
            self.dy * other.dz - self.dz * other.dy,
            self.dz * other.dx - self.dx * other.dz,
            self.dx * other.dy - self.dy * other.dx
        )

    def scale(self, factor):
        self.dx *= factor
        self.dy *= factor
        self.dz *= factor

    def add(self, other):
        self.dx += other.dx
        self.dy += other.dy
        self.dz += other.dz

    def subtract(self, other):
        self.dx -= other.dx
        self.dy -= other.dy
        self.dz -= other.dz

    def __add__(self, other):
        return Vector3(self.dx + other.dx, self.dy + other.dy, self.dz + other.dz)

    def __sub__(self, other):
        return Vector3(self.dx - other.dx, self.dy - other.dy, self.dz - other.dz)

    def __mul__(self, factor):
        return Vector3(self.dx * factor, self.dy * factor, self.dz * factor)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __truediv__(self, factor):
        return Vector3(self.dx / factor, self.dy / factor, self.dz / factor)

    def __repr__(self):
        return f"Vector3({self.dx:.5f}, {self.dy:.5f}, {self.dz:.5f})"
