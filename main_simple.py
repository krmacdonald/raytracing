"""
A basic (but far from simple) ray tracer.

Author: Christian Duncan
Course: CSC345/645: Computer Graphics
Term: Fall 2024

This code provides the main interface to a ray tracing project. It allows navigation of a simple
scene and then the ability to render that scene using ray tracing. The implementation is SLOW.
But making it efficient is an entirely more complex task.
"""

import sys
import math
import pygame
import copy
from OpenGL.GLU import *
from OpenGL.GL import *
from Navigator import Navigator
from Camera import Camera
from Point3 import Point3
from Vector3 import Vector3
from Window import Window
from Scene import Scene
from SphereObj import SphereObj
from BoxObj import BoxObj
from Material import Material
from Light import Light
from Color import Color

# Constants
FPS = 60
FRAME_WIDTH = 500
FRAME_HEIGHT = 500
FRAME_TITLE = "Go Ray Tracer!"
# DELAY = int(1000 / FPS)

# Initialize global variables
init_eye = Point3(0, 0, 10)
init_look = Point3(0, 0, 0)
init_up = Vector3(0, 1, 0)
init_view_angle = 45.0
init_near = 0.1
init_far = 50.0

nav = Navigator(Camera(init_eye, init_look, init_up))
win = Window(FRAME_WIDTH, FRAME_HEIGHT, FRAME_TITLE)
scn = Scene()
light_angle = 0
light_speed = 1
light_distance = 5
animate = True  # Animation

# Enums for rendering modes
RENDER_SOLID = 0
RENDER_RAY_SINGLE = 1
RENDER_RAY_RECORD = 2
render_mode = RENDER_SOLID
raytrace_count = 0  # How many ray traced images have been generated so far

block_size = 4

# Functions
def set_light_positions(lightA):
    global light_angle, light_distance
    pos_x = light_distance * math.cos(math.radians(light_angle))
    pos_y = light_distance * math.sin(math.radians(light_angle))
    pos_z = 0

    lightA.set_position(pos_x, pos_y, pos_z)
    lightA.obj.reset()
    lightA.obj.translate(pos_x, pos_y, pos_z)
    lightA.obj.scale(0.2, 0.2, 0.2)

def init_scene():
    global scn, nav, lightA

    # Setup camera
    cam = nav.get_camera()
    cam.look_at(init_eye, init_look, init_up)
    cam.set_lens_shape(init_view_angle, FRAME_WIDTH / FRAME_HEIGHT, init_near, init_far)

    # Create objects and add them to the scene
    mat = Material()
    mat.set_copper()
    mat.set_reflectivity(0.1)
    ball = SphereObj()
    ball.set_material(mat)
    ball.translate(0,1,0)
    ball.scale(1, 2, 1)
    ball.name = "Ball 1"
    scn.add_object(ball)

    mat = Material()
    mat.set_silver()
    mat.set_reflectivity(0.8)
    floor = BoxObj()
    floor.name = "Floor"
    floor.set_material(mat)
    floor.translate(0, -2, 0)
    floor.scale(10, 0.1, 10)
    scn.add_object(floor)

    mat1 = Material()
    mat1.set_pewter()
    mat1.set_reflectivity(0.1)
    ceiling = BoxObj()
    ceiling.name = "Ceiling"
    ceiling.set_material(mat1)
    ceiling.translate(0, 5, 0)
    ceiling.scale(10, 0.1, 10)
    scn.add_object(ceiling)

    wallmat = Material()
    wallmat.set_gold()
    wall = BoxObj()
    wall.name = "Wall"
    wall.set_material(wallmat)
    wall.translate(10, -2, 0)
    wall.scale(10, .1, 10)
    wall.rotate(90, Vector3(0, 0, 0))
    scn.add_object(wall)
    

    # Light setup
    lightA = Light()
    scn.add_light(lightA)
    mat = Material()
    mat.set_emissive_only(lightA.get_diffuse())
    mat.set_translucent(True)

    # Create a visible component of the light
    # It will be associated both with the light and with the Scene
    lightA.obj = SphereObj()
    lightA.obj.name = "Light Source"
    lightA.obj.set_material(mat)
    scn.add_object(lightA.obj)

    set_light_positions(lightA)

# Return a copy of all the things in scene that could have changed!
def get_copy_state():
    return (copy.deepcopy(nav.camera), light_angle)

# Reset the state back to the given state
def restore_state(state):
    global nav, light_angle, lightA
    nav.camera = copy.deepcopy(state[0])
    light_angle = state[1]
    set_light_positions(lightA)

def display():
    global render_mode, raytrace_count, animate, record
    if render_mode == RENDER_SOLID:
        scn.render_solid(nav.get_camera(), win)
        pygame.display.flip()
    elif render_mode == RENDER_RAY_SINGLE:
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        scn.render_ray_traced(nav.get_camera(), win, block_size)
        win.save_pixmap('image{0}.png'.format(raytrace_count))
        raytrace_count+=1
        animate = False
        render_mode = RENDER_SOLID # So doesn't try to render it again!
        pygame.event.clear() # Takes so long to render, need to clear events that happened while rendering!
    elif render_mode == RENDER_RAY_RECORD:
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        if len(record) < 60: # Capped so we don't go crazy ray tracing here!
            # Save a copy of the things that could change from scene to scene
            record.append(get_copy_state())

# Ray trace a sequence of frames - each step recorded to recreate
def raytrace_records(record):
    # Save the current state
    save_state = get_copy_state()

    record_count = 1
    for s in record:
        print("Recording frame {0} of {1}".format(record_count, len(record)))
        # Restore state back to this saved record
        restore_state(s)
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        scn.render_ray_traced(nav.get_camera(), win, block_size)
        win.save_pixmap('frame{0}.png'.format(record_count))
        record_count+=1

    pygame.event.clear() # Takes so long to render, need to clear events that happened while rendering!

    # Restore it back
    restore_state(save_state)

def handle_events():
    global render_mode, block_size, light_speed, animate, record
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_1:
                print("BLOCK SIZE 1")
                block_size = 1
            elif event.key == pygame.K_2:
                print("BLOCK SIZE 2")
                block_size = 2
            elif event.key == pygame.K_3:
                print("BLOCK SIZE 4")
                block_size = 4
            elif event.key == pygame.K_4:
                print("RENDER RAY SINGLE MODE")
                render_mode = RENDER_RAY_SINGLE
            elif event.key == pygame.K_BACKSLASH:
                print("RENDER RAY RECORD MODE")
                if render_mode != RENDER_RAY_RECORD:
                    # Start the recording!
                    record = []
                    render_mode = RENDER_RAY_RECORD
                else:
                    # End it and begin ray tracing each image
                    raytrace_records(record)
                    render_mode = RENDER_SOLID
                    print("RENDER SOLID MODE 1")
                    animate = False
                    render_mode = RENDER_SOLID # So doesn't try to render it again!
                    print("RENDER SOLID MODE 2")
            elif event.key == pygame.K_SPACE:
                animate = not animate
            elif event.key == pygame.K_PERIOD:
                light_speed = 0
            else:
                nav.keyboard(event.key)
    return True

def main():
    global light_angle, light_distance, lightA, render_mode, animate
    win.initialize()
    init_scene()

    clock = pygame.time.Clock()
    running = True

    # Set up lighting and depth-test
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)    # Inefficient...
    glEnable(GL_DEPTH_TEST)   # For z-buffering!

    while running:
        running = handle_events()

        if animate:
            # Advance the navigator
            nav.advance()
   
            # Do any other animations needed (like moving objects around)
            # Move the main light around
            light_angle += light_speed
            if light_angle >= 360: light_angle -= 360
            elif light_angle < 0: light_angle += 360

            set_light_positions(lightA)

        display()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
