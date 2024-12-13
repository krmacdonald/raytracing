
import pygame
from pygame.locals import *
from OpenGL.GL import *
from RGBPixmap import RGBPixmap

class Window:
    def __init__(self, width, height, title="PyGame Window"):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None
        self.pixmap = RGBPixmap(self.height, self.width)

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.OPENGL)
        pygame.display.set_caption(self.title)
        pygame.key.set_repeat(300, 50)  # Key repeat rate

    def clear(self, color=(0, 0, 0)):
        # Clear the screen with a given color (default is black)
        if self.screen:
            self.screen.fill(color)

    def draw_pixel(self, row, col, color, block_size=1):
        # Write a pixel of given block_size IN THE PIXMAP Array
        self.pixmap.set_pixel(row, col, color, block_size)

    def save_pixmap(self, filename):
        surface = pygame.Surface((self.width, self.height))
        self.pixmap.copy_to_surface(surface)
        pygame.image.save(surface, filename)
        print("Rendered image saved as '{0}'".format(filename))

    def prepare_window(self):
        glViewport(0, 0, self.width, self.height)

        # Clear the screen
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

