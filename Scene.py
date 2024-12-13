import math
from GeomObj import GeomObj
from Light import Light
from Hit import Hit
from Ray import Ray
from Color import Color
from Vector3 import Vector3
from OpenGL.GL import *

class Scene:
    def __init__(self, background_color=None):
        self.objects = []  # List of geometric objects in the scene
        self.lights = []  # List of lights in the scene
        self.background = Color(0, 0, 0, 1) if background_color is None else background_color
        self.reflection_adjustment = 0.01
        self.max_reflection_depth = 3
        self.reflective_coeff_cutoff = 0.05

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def render_solid(self, camera, window):
        glEnable(GL_DEPTH_TEST)

        window.prepare_window()
   
        glColor3f(1.0,1.0,1.0);   
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity();
   
        # Prepare our camera (which is "attached" to the plane)
        camera.prepare_camera()

        for light in self.lights:
            light.enable()

        for obj in self.objects:
            obj.prepare_solid()
            obj.render_solid()
            obj.done_solid()
        glFlush()

    def render_ray_traced(self, camera, window, block_size=1):
        width, height = window.width, window.height
        total_blocks = (width // block_size) * (height // block_size)
        completed_blocks = 0

        N = camera.near_dist
        H = N * math.tan(math.radians(camera.angle/2))
        W = H * camera.aspect_ratio
        deltaC = 2*W/width * block_size
        deltaR = 2*H/height * block_size
        ray = Ray(camera.eye, camera.n.__mul__(-1))

        next_prog_report = 0
        print("Camera: eye={0}, u={1}, v={2}, n={3}".format(camera.eye, camera.u, camera.v, camera.n))
        vr = H
        for row in range(0, height, block_size): 
            uc = -W
            for col in range(0, width, block_size):
                # Create ray
                ray.dir = camera.n.__mul__(-N)
                ray.dir.add(camera.u.__mul__(uc))
                ray.dir.add(camera.v.__mul__(vr))

                # Compute ray intersection with scene
                temp_color = self.shade(ray)
                temp_color.cap() # Make sure no value is >1
                window.draw_pixel(row, col, temp_color, block_size)

                completed_blocks += 1
                progress = (completed_blocks / total_blocks) * 100
                if progress >= next_prog_report:
                    print(f"Ray tracing progress: {progress:.2f}%")
                    next_prog_report += 10
                uc += deltaC
            vr -= deltaR
            
    def intersect(self, ray, best_hit, skip_translucent=False, just_one=False, ignore=[]):
        for obj in self.objects:
            if obj not in ignore and (not skip_translucent or not obj.material.is_translucent()):
                if obj.intersect(ray, best_hit) and just_one:
                    return True  # Stop the moment we find ANY intersection (for shadows)

    """
    * shade:
    *     r: The ray to be traced and shaded
    *     depth: Used to prevent multiple passes of reflections (a base cutoff)
    *     reflectiveCoefficient: a much better means of cutting off reflection recursion based on accumulate "worth" of the reflection
    *         That is, imagine a material with reflectivity 0.1 - once reflected any color has only 0.1 strength - a second
    *         reflection off same material would have an influence of only 0.01 and yet again just 0.001 - most likely quite insignificant!
    *     returns the color
    """
    def shade(self, ray, depth=0, reflective_coefficient=1.0, ignore=[]):
        # print("DEBUG: Shade method: Ray: {0}".format(ray))
        color = Color()
        best_hit = Hit()
        self.intersect(ray, best_hit, ignore=ignore)

        if best_hit.t != -1:
            # print("Ray: {0} intersected: {1}".format(ray, best_hit.obj.name))
            mat = best_hit.obj.material  # The material property of the object hit
            norm = best_hit.norm         # Normal to surface at this location
            norm.normalize()             # Make sure the normal is normalized (unit length)
            color.set(mat.get_emissive())
            global_ambient = Color()
            global_ambient.set(Light.get_global_ambient())
            global_ambient.mult(mat.get_ambient())
            color.add(global_ambient)

            for light in self.lights:
                # Calculate the color from this light using Phong Illumination model
                light_color = Color()

                # Starting with ambient (shadow doesn't matter here)
                light_color.set(light.get_ambient())
                light_color.mult(mat.get_ambient())

                # See if the object is in shadow from this list
                shadow = light.compute_shadow(self, best_hit)
                if shadow > 0:
                    lpos = light.get_position()                    
                    w = lpos[3]
                    if w == 0:
                        # Light is a directional light (the "position" gives light direction)
                        s = Vector3(lpos[0], lpos[1], lpos[2])
                    else:
                        # Light is point source
                        s = Vector3(lpos[0]/w - best_hit.point.x, lpos[1]/w - best_hit.point.y, lpos[2]/w - best_hit.point.z)
                    
                    v = Vector3.from_points(best_hit.point, ray.get_source())  # From hit point to "Eye" (ray source)
                    s.normalize()
                    v.normalize()

                    # Compute the Halfway Vector between s and v
                    h = Vector3(s.dx + v.dx, s.dy + v.dy, s.dz + v.dz)
                    h.normalize()

                    # Ready to compute lambertian portion (from diffuse)
                    lambert = s.dot(norm)
                    if lambert > 0:
                        diff_color = Color()
                        diff_color.set(light.get_diffuse())
                        diff_color.mult(mat.get_diffuse())
                        diff_color.dim(lambert)
                        light_color.add(diff_color)

                        phong = h.dot(norm)
                        if phong > 0:
                            spec_color = Color()
                            spec_color.set(light.get_specular())
                            spec_color.mult(mat.get_specular())
                            spec_color.dim(math.pow(phong, mat.get_shininess()))
                            light_color.add(spec_color)

                color.add(light_color)

            reflective_coefficient *= mat.get_reflectivity()
            if reflective_coefficient > self.reflective_coeff_cutoff and depth < self.max_reflection_depth:
                # Material is reflective and its reflection actually makes a significant impact
                # This is currently based on the reflectivity coefficient (accumulated over each recursive level)
                reflection_ray = ray.compute_reflection(best_hit.point, best_hit.norm)

                # Ignore the object reflecting off or might think ray hits it immediately due to round-off err
                ignore = [best_hit.obj]
                reflection_color = self.shade(reflection_ray, depth + 1, reflective_coefficient, ignore=ignore)
                color.add_mix(reflection_color, mat.get_reflectivity())
        else:
            color.set(self.background)
    
        return color
    