
from Color import Color
from OpenGL.GL import glMaterialfv, GL_FRONT_AND_BACK, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_EMISSION, GL_SHININESS

class Material:
    def __init__(self, emissive=None, ambient=None, diffuse=None, specular=None, shininess=1.0, reflectivity=0.0, translucent=False):
        self.emissive = emissive if emissive else Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = ambient if ambient else Color(0.2, 0.2, 0.2, 1.0)
        self.diffuse = diffuse if diffuse else Color(0.8, 0.8, 0.8, 1.0)
        self.specular = specular if specular else Color(1.0, 1.0, 1.0, 1.0)
        self.shininess = shininess
        self.reflectivity = reflectivity
        self.translucent = translucent

    def set_emissive(self, color):
        self.emissive = color

    def set_ambient(self, color):
        self.ambient = color

    def set_diffuse(self, color):
        self.diffuse = color

    def set_specular(self, color):
        self.specular = color

    def set_shininess(self, value):
        self.shininess = value

    def set_reflectivity(self, value):
        self.reflectivity = value

    def set_translucent(self, is_translucent):
        self.translucent = is_translucent

    def get_emissive(self):
        return self.emissive

    def get_ambient(self):
        return self.ambient

    def get_diffuse(self):
        return self.diffuse

    def get_specular(self):
        return self.specular

    def get_shininess(self):
        return self.shininess

    def get_reflectivity(self):
        return self.reflectivity

    def is_translucent(self):
        return self.translucent

    def set_gold(self):
        self.emissive = Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = Color(0.24725, 0.1995, 0.0745, 1.0)
        self.diffuse = Color(0.75164, 0.60648, 0.22648, 1.0)
        self.specular = Color(0.628281, 0.555802, 0.366065, 1.0)
        self.shininess = 51.2

    def set_silver(self):
        self.emissive = Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = Color(0.19225, 0.19225, 0.19225, 1.0)
        self.diffuse = Color(0.50754, 0.50754, 0.50754, 1.0)
        self.specular = Color(0.508273, 0.508273, 0.508273, 1.0)
        self.shininess = 51.2

    def set_chrome(self):
        self.emissive = Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = Color(0.25, 0.25, 0.25)
        self.diffuse = Color(0.4, 0.4, 0.4)
        self.specular = Color(0.774597, 0.774597, 0.774597)
        self.exponent = 76.8

    def set_copper(self):
        self.emissive = Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = Color(0.19125, 0.0735, 0.0225, 1.0)
        self.diffuse = Color(0.7038, 0.27048, 0.0828, 1.0)
        self.specular = Color(0.256777, 0.137622, 0.086014, 1.0)
        self.shininess = 12.8

    def set_pewter(self):
        self.emissive = Color(0.0, 0.0, 0.0, 1.0)
        self.ambient = Color(0.10588, 0.058824, 0.113725, 1.0)
        self.diffuse = Color(0.427451, 0.470588, 0.541176, 1.0)
        self.specular = Color(0.3333, 0.3333, 0.521569, 1.0)
        self.shininess = 9.84615

    def set_emissive_only(self, color):
        self.emissive = color
        self.ambient = Color(0.0, 0.0, 0.0, 1.0)
        self.diffuse = Color(0.0, 0.0, 0.0, 1.0)
        self.specular = Color(0.0, 0.0, 0.0, 1.0)
        self.shininess = 1.0

    def set_material_OpenGL(self):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [self.ambient.rgba[0], self.ambient.rgba[1], self.ambient.rgba[2], self.ambient.rgba[3]])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [self.diffuse.rgba[0], self.diffuse.rgba[1], self.diffuse.rgba[2], self.diffuse.rgba[3]])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [self.specular.rgba[0], self.specular.rgba[1], self.specular.rgba[2], self.specular.rgba[3]])
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [self.emissive.rgba[0], self.emissive.rgba[1], self.emissive.rgba[2], self.emissive.rgba[3]])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [self.shininess])

    def __repr__(self):
        return (
            f"Material(Emissive: {self.emissive}, Ambient: {self.ambient}, "
            f"Diffuse: {self.diffuse}, Specular: {self.specular}, "
            f"Shininess: {self.shininess}, Reflectivity: {self.reflectivity}, "
            f"Translucent: {self.translucent})"
        )
