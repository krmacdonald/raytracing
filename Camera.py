import math
from Vector3 import Vector3
from Point3 import Point3
from OpenGL.GL import glLoadMatrixf, glMatrixMode, glLoadIdentity, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective

class Camera:
    def __init__(self, eye=None, look=None, up=None, angle=45, aspect_ratio=1.33, near_dist=0.1, far_dist=1000.0):
        self.eye = eye if eye else Point3()
        self.look = look if look else Point3(0, 0, -1)
        self.up = up if up else Vector3(0, 1, 0)
        self.angle = angle
        self.aspect_ratio = aspect_ratio
        self.near_dist = near_dist
        self.far_dist = far_dist
        self.update_camera()
        
    def update_camera(self):
        self.n = Vector3.from_points(self.look, self.eye)
        self.n.normalize()
        self.u = Vector3.cross(self.up, self.n)
        self.u.normalize()
        self.v = Vector3.cross(self.n, self.u)

    def look_at(self, eye, look, up):
        self.eye = eye
        self.look = look
        self.up = up
        self.update_camera()

    def set_lens_shape(self, angle, aspect_ratio, near_dist, far_dist):
        self.angle = angle
        self.aspect_ratio = aspect_ratio
        self.near_dist = near_dist
        self.far_dist = far_dist

    def slide(self, du, dv, dn):
        self.eye.x += du * self.u.dx + dv * self.v.dx + dn * self.n.dx
        self.eye.y += du * self.u.dy + dv * self.v.dy + dn * self.n.dy
        self.eye.z += du * self.u.dz + dv * self.v.dz + dn * self.n.dz

    # Helper function to rotate vectors a and b by a degree delta
    # Updates the two vectors given
    @staticmethod
    def rotate(delta, a, b):
        rad = math.radians(delta)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)
        (dx, dy, dz) = (a.dx, a.dy, a.dz)
        (a.dx, a.dy, a.dz) = (cos_rad*dx + sin_rad*b.dx, cos_rad*dy + sin_rad*b.dy, cos_rad*dz + sin_rad*b.dz)
        (b.dx, b.dy, b.dz) = (-sin_rad*dx + cos_rad*b.dx, -sin_rad*dy + cos_rad*b.dy, -sin_rad*dz + cos_rad*b.dz)

    def yaw(self, angle):
        Camera.rotate(angle, self.n, self.u)

    def pitch(self, angle):
        Camera.rotate(angle, self.v, self.n)

    def roll(self, angle):
        Camera.rotate(angle, self.u, self.v)

    def set_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.angle, self.aspect_ratio, self.near_dist, self.far_dist)

    def set_model_view_matrix(self):
        glMatrixMode(GL_MODELVIEW)
        view_matrix = [
            self.u.dx, self.v.dx, self.n.dx, 0.0,
            self.u.dy, self.v.dy, self.n.dy, 0.0,
            self.u.dz, self.v.dz, self.n.dz, 0.0,
            -Vector3.dot(self.u, Vector3.from_points(Point3(0, 0, 0), self.eye)),
            -Vector3.dot(self.v, Vector3.from_points(Point3(0, 0, 0), self.eye)),
            -Vector3.dot(self.n, Vector3.from_points(Point3(0, 0, 0), self.eye)), 1.0
        ]
        glLoadMatrixf(view_matrix)

    """
        prepareCamera():
        Prepares the camera for OpenGL calls.
        This sets the Project Matrix to Camera's shape
        and the MV Matrix to appropriate one given values u,v,n, and eye
    """
    def prepare_camera(self):
        self.set_projection()
        self.set_model_view_matrix()

    def get_eye(self):
        return self.eye

    def get_near_dist(self):
        return self.near_dist

    def get_view_angle(self):
        return self.angle

    def get_aspect_ratio(self):
        return self.aspect_ratio

    def __repr__(self):
        return f"Camera(Eye: {self.eye}, Look: {self.look}, Up: {self.up})"
