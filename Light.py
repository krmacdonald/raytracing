
from Color import Color
from Ray import Ray
from Hit import Hit
from Point3 import Point3
from Vector3 import Vector3
from OpenGL.GL import *

class Light:
    SHADOW_ADJUSTMENT = 0.0001
    globalAmbient = Color(1.0, 1.0, 1.0, 1.0)

    def __init__(self, position=None, ambient=None, diffuse=None, specular=None, id=GL_LIGHT0):
        self.position = [0.0, 0.0, 0.0, 1.0] if position is None else position
        self.ambient = Color(0.2, 0.2, 0.2, 1.0) if ambient is None else ambient
        self.diffuse = Color(1.0, 1.0, 1.0, 1.0) if diffuse is None else diffuse
        self.specular = Color(1.0, 1.0, 1.0, 1.0) if specular is None else specular
        self.light_id = id
        self.obj = None  # The "object" associated with this light

    @staticmethod
    def start_light_processing_OpenGL():
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)  # Otherwise scaling really screws with normals (and their affect on lighting)
        glShadeModel(GL_SMOOTH)
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, Light.globalAmbient.getColor())

    @staticmethod
    def set_global_ambient(ambient):
        Light.globalAmbient = ambient

    @staticmethod
    def get_global_ambient():
        return Light.globalAmbient

    def set_position(self, x, y, z, w=1.0):
        self.position = [x, y, z, w]

    def get_position(self):
        return self.position

    def set_ambient(self, color):
        self.ambient = color

    def set_diffuse(self, color):
        self.diffuse = color

    def set_specular(self, color):
        self.specular = color

    def get_ambient(self):
        return self.ambient

    def get_diffuse(self):
        return self.diffuse

    def get_specular(self):
        return self.specular

    def enable(self):
        glEnable(self.light_id)
        glLightfv(self.light_id, GL_AMBIENT, [self.ambient.rgba[0], self.ambient.rgba[1], self.ambient.rgba[2], self.ambient.rgba[3]])
        glLightfv(self.light_id, GL_DIFFUSE, [self.diffuse.rgba[0], self.diffuse.rgba[1], self.diffuse.rgba[2], self.diffuse.rgba[3]])
        glLightfv(self.light_id, GL_SPECULAR, [self.specular.rgba[0], self.specular.rgba[1], self.specular.rgba[2], self.specular.rgba[3]])
        glLightfv(self.light_id, GL_POSITION, self.position)

    def compute_shadow(self, scene, hit):
        # Determine if there is an object in the way from hit.point to light's position/direction
        first_hit = Hit()
        if self.position[3] != 0:  # Positional light
            first_hit.t = 1 # Stop the search at the light source # Directional light

        # We will test a ray from object (hit.point) to the light (infinitely far away or at t=1)
        ray = Ray(hit.point.__copy__(), Vector3(self.position[0], self.position[1], self.position[2]))
        ignore_list = [self.obj, hit.obj] # Objects to skip in intersection test
        return 0 if scene.intersect(ray, first_hit, skip_translucent=True, just_one=True, ignore=ignore_list) else 1
 
    def __repr__(self):
        return f"Light(Position: {self.position}, Ambient: {self.ambient}, Diffuse: {self.diffuse}, Specular: {self.specular})"
