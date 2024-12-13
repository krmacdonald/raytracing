
import math
import pygame
from Camera import Camera

class Navigator:
    def __init__(self, camera, delta_yaw=1.0, delta_pitch=1.0, delta_roll=1.0, delta_step=1.0):
        self.camera = camera
        self.delta_yaw = delta_yaw
        self.delta_pitch = delta_pitch
        self.delta_roll = delta_roll
        self.delta_step = delta_step
        self.speed = 0
        self.delta_speed = 0.01
        self.running = True

    def get_camera(self):
        return self.camera

    def keyboard(self, key):
        # Handle keyboard input for camera movement
        if key == ord('='):
            self.throttle_up()
        elif key == ord('-'):
            self.throttle_down()
        elif key == ord('/'):
            self.stop()
        elif key == pygame.K_LEFT:
            self.yaw(self.delta_yaw)
        elif key == pygame.K_RIGHT:
            self.yaw(-self.delta_yaw)
        elif key == pygame.K_UP:
            self.pitch(self.delta_pitch)
        elif key == pygame.K_DOWN:
            self.pitch(-self.delta_pitch)
        elif key == ord('w'):
            self.camera.slide(0, 0, -self.delta_step)
        elif key == ord('s'):
            self.camera.slide(0, 0, self.delta_step)
        elif key == ord('a'):
            self.camera.slide(-self.delta_step, 0, 0)
        elif key == ord('d'):
            self.camera.slide(self.delta_step, 0, 0)
        elif key == ord('q'):
            self.camera.slide(0, self.delta_step, 0)
        elif key == ord('e'):
            self.camera.slide(0, -self.delta_step, 0)
        elif key == ord('h'):
            self.display_instructions()

    def advance(self):
        self.camera.slide(0, 0, -self.speed)

    def yaw(self, angle):
        self.camera.yaw(angle)

    def pitch(self, angle):
        self.camera.pitch(angle)

    def roll(self, angle):
        self.camera.roll(angle)

    def throttle_up(self):
        self.speed += self.delta_speed

    def throttle_down(self):
        self.speed -= self.delta_speed

    def stop(self):
        self.speed = 0

    def display_instructions(self):
        print("=" * 60)
        print("Navigator Instructions:")
        print("  +/-:        Adjust throttle")
        print("  wasd:       Slide forward, left, backward, right")
        print("  h:          Display help")
        print("  Arrow keys: Adjust pitch/yaw")
        print("  ESC:        Exit application")
        print("=" * 60)
