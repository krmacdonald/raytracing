
class Point3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __copy__(self): return Point3(self.x, self.y,  self.z)

    @staticmethod
    def lerp(p, v, t):
        # Linear interpolation between a point and vector
        return Point3(p.x + t * v.dx, p.y + t * v.dy, p.z + t * v.dz)

    def render(self):
        # Placeholder for rendering functionality
        print(f"Render Point: ({self.x}, {self.y}, {self.z})")

    def __repr__(self):
        return f"Point3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
