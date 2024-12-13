
from Matrix import Matrix
from Material import Material
from Ray import Ray
from Hit import Hit
from OpenGL.GL import *

class GeomObj:
    def __init__(self):
        self.material = Material()
        self.matrix = Matrix()
        self.matrix_inverse = Matrix()
        self.matrix.load_identity()
        self.matrix_inverse.load_identity()
        self.name = "Unknown"   # Use a name to help identify the object for debugging

    def prepare_solid(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(self.matrix.m)
   
        # Prepare Material property
        self.material.set_material_OpenGL()

    def done_solid(self):
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def set_material(self, material):
        self.material = material

    def translate(self, dx, dy, dz):
        self.matrix.post_translate(dx, dy, dz)
        self.matrix_inverse.pre_translate(-dx, -dy, -dz)

    def scale(self, sx, sy, sz):
        self.matrix.post_scale(sx, sy, sz)
        self.matrix_inverse.pre_scale(1.0 / sx, 1.0 / sy, 1.0 / sz)

    def rotate(self, angle, axis):
        self.matrix.post_rotate(angle, axis)
        self.matrix_inverse.pre_rotate(-angle, axis)

    def intersect(self, ray, best_hit):
        transformed_ray = Ray(
            self.matrix_inverse.affine_mult_point(ray.source),
            self.matrix_inverse.affine_mult_vector(ray.dir)
        )
        if self.local_intersect(transformed_ray, best_hit):
            # Need to recompute the hit point in WORLD SPACE (using original ray)
            best_hit.point = ray.eval(best_hit.t)

            # Transform the normal in best_hit from OBJECT space to WORLD space
            # using the inverse transpose
            best_hit.norm = self.matrix_inverse.affine_transpose_mult_vector(best_hit.norm)
            best_hit.norm.normalize()
            return True
        return False

    """
      * Should be defined for each subclass of GeomObj.
      *    ray: Defined in the Object's space
      *    best_hit: Current best hit time
      *    returns: true if a closer hit was found
      *    IN ADDITION: If a closer hit was found then:
      *       1) best_hit.t should have the new hit "time"
      *       2) best_hit.point should have the point location (IN OBJECT SPACE) of the intersection
      *       3) best_hit.norm should contain normal at intersection (IN OBJECT SPACE)
      *       4) best_hit.obj should reference the object hit itself (self)
    """
    def local_intersect(self, ray, best_hit):
        raise NotImplementedError("Subclasses must implement local_intersect.")
