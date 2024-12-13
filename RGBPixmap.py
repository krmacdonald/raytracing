import pygame
import numpy as np
from OpenGL.GL import *

class RGBPixmap:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.pixel = np.zeros((self.n_cols, self.n_rows, 4), dtype=np.float32)

    def resize(self, n_rows, n_cols):
        """ Could resize this more efficiently! Numpy supports resizing I believe but for now creating new array."""
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.pixel = np.zeros((self.n_cols, self.n_rows, 4), dtype=np.float32)

    def set_pixel(self, row, col, color, block_size=1):
        self.pixel[col:col+block_size, row:row+block_size] = color.rgba

    def copy_to_surface(self, surface):
        """ Copy the current pixel array to the PyGame surface for displaying"""
        # Convert the array to uint8 for Pygame
        pixel_array_uint8 = (self.pixel * 255).astype(np.uint8)

        # Create a Pygame surface and fill it with the pixel array
        pygame.surfarray.blit_array(surface, pixel_array_uint8[:, :, :3])  # Use only RGB values for the surface
