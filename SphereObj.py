
from GeomObj import GeomObj
from Ray import Ray
from Hit import Hit
from Point3 import Point3
from Vector3 import Vector3
from OpenGL.GLU import *

class SphereObj(GeomObj):
    def __init__(self, resolution=100):
        super().__init__()
        self.ball = gluNewQuadric()
        self.resolution = resolution
        gluQuadricDrawStyle(self.ball, GLU_FILL)

    def render_solid(self):
        gluSphere(self.ball, 1, self.resolution, self.resolution)

    def render_wire(self):
        print("Rendering wireframe sphere. Placeholder for rendering logic.")

    def reset(self):
        # Reset the sphere's transformations
        self.matrix.load_identity()
        self.matrix_inverse.load_identity()

    def local_intersect(self, ray, best_hit):
        s = ray.source
        c = ray.dir
        A = c.dx ** 2 + c.dy ** 2 + c.dz ** 2
        B = 2 * (s.x * c.dx + s.y * c.dy + s.z * c.dz)
        C = s.x ** 2 + s.y ** 2 + s.z ** 2 - 1
        discriminant = B ** 2 - 4 * A * C

        if discriminant < 0:
            return False

        sqrt_disc = discriminant ** 0.5
        t1 = (-B - sqrt_disc) / (2 * A)
        t2 = (-B + sqrt_disc) / (2 * A)
        t = min(t1, t2) if t1 > 0 and t2 > 0 else max(t1, t2)

        if t < 0 or (t >= best_hit.t and best_hit.t != -1):
            return False

        best_hit.t = t
        best_hit.point = ray.eval(t)
        best_hit.norm = Vector3(best_hit.point.x, best_hit.point.y, best_hit.point.z)
        best_hit.norm.normalize()
        best_hit.obj = self
        return True
