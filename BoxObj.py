from GeomObj import GeomObj
from Vector3 import Vector3
from Hit import Hit
from OpenGL.GL import *

class BoxObj(GeomObj):
    def __init__(self):
        super().__init__()

    @staticmethod
    def draw_side(slices_x, slices_y):
        """ Draw a plane of the specified dimension.
            The plane is a 2x2 square centered at origin (coordinates go -1 to 1).
            slices_x and slices_y are the number of divisions in each dimension
        """
        dx = 2 / slices_x  # Change in x direction
        dy = 2 / slices_y  # Change in y direction

        glNormal3f(0, 0, 1)
        y = -1
        for j in range(slices_y):
            glBegin(GL_TRIANGLE_STRIP)
            cx = -1
            for i in range(slices_x):
                glVertex3f(cx, y + dy, 0)
                glVertex3f(cx, y, 0)
                cx += dx
            glVertex3f(1, y + dy, 0)
            glVertex3f(1, y, 0)
            glEnd()
            y += dy

    def render_solid(self, slices=10):
        """ Draw a unit cube with one corner at origin in positive octant."""
        # Draw side 1 (Front)
        glPushMatrix()
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 2 (Back)
        glPushMatrix()
        glRotated(180, 0, 1, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 3 (Left)
        glPushMatrix()
        glRotatef(-90, 0, 1, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 4 (Right)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 5 (Top)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 6 (Bottom)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

    def local_intersect(self, ray, best_hit):
        t_min = -float('inf')
        t_max = float('inf')

        for i in range(3):
            origin = getattr(ray.source, "xyz"[i])
            direction = getattr(ray.dir, "dx dy dz".split()[i])
            
            if abs(direction) < 1e-6:
                if not (-1 <= origin <= 1):
                    return False
            else:
                t1 = (-1 - origin) / direction
                t2 = (1 - origin) / direction
                t_near, t_far = min(t1, t2), max(t1, t2)

                t_min = max(t_min, t_near)
                t_max = min(t_max, t_far)

                if t_min < t_max:
                    return False

        t = t_min if t_min > 0 else t_max

        if t < 0 or (t >= best_hit.t and best_hit.t != -1):
            return False

        best_hit.t = t
        best_hit.point = ray.eval(t)
        best_hit.norm = self.compute_normal(best_hit.point)
        best_hit.obj = self
        return True

    def compute_normal(self, point):
        """ Compute the normal vector at the intersection point.
            point: The intersection point.
            returns: The normal vector at the intersection point.
        """
        normal = Vector3(0, 0, 0)
        if abs(point.x - (-1)) < 1e-6:
            normal.x = -1
        elif abs(point.x - 1) < 1e-6:
            normal.x = 1
        elif abs(point.y - (-1)) < 1e-6:
            normal.y = -1
        elif abs(point.y - 1) < 1e-6:
            normal.y = 1
        elif abs(point.z - (-1)) < 1e-6:
            normal.z = -1
        elif abs(point.z - 1) < 1e-6:
            normal.z = 1
        return normal
