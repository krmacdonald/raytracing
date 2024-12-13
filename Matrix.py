"""
Author: Christian Duncan
CSC345/645: Computer Graphics
Fall 2024

This class represent a 4x4 affine matrix stored in Column-Major order.
Methods are provided for translating, scaling, and rotating 
and doing so either pre or post multiplication.
"""
import math
from Point3 import Point3
from Vector3 import Vector3

class Matrix:
    def __init__(self):
        self.m = [0] * 16  # Initialize a 4x4 matrix as a flat list

    def load_identity(self):
        # Load identity matrix
        self.m = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ]

    def set(self, other):
        # Copy matrix contents
        self.m = other.m[:]

    def set_translate(self, dx, dy, dz):
        # Set translation matrix
        self.m = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            dx, dy, dz, 1
        ]

    def set_scale(self, sx, sy, sz):
        # Set scale matrix
        self.m = [
            sx, 0,  0,  0,
            0,  sy, 0,  0,
            0,  0,  sz, 0,
            0,  0,  0,  1
        ]

    def set_rotate(self, angle, vec):
        # Set rotation matrix based on angle and vector
        rad_angle = math.radians(angle)
        c = math.cos(rad_angle)
        s = math.sin(rad_angle)
        dx, dy, dz = vec.dx, vec.dy, vec.dz

        self.m = [
            c + (1 - c) * dx * dx,
            (1 - c) * dx * dy + s * dz,
            (1 - c) * dx * dz - s * dy,
            0,
            (1 - c) * dx * dy - s * dz,
            c + (1 - c) * dy * dy,
            (1 - c) * dy * dz + s * dx,
            0,
            (1 - c) * dx * dz + s * dy,
            (1 - c) * dy * dz - s * dx,
            c + (1 - c) * dz * dz,
            0,
            0, 0, 0, 1
        ]

    @staticmethod
    def multiply(a, b):
        # Multiply the two matrices: a*b, returns result
        result = [0] * 16
        for row in range(4):
            for col in range(4):
                result[row + col * 4] = sum(
                    a.m[row + k * 4] * b.m[k + col * 4] for k in range(4)
                )
        return result

    def post_mult_set(self, other):
        # Post-multiply this matrix with another matrix and store the result in this matrix
        # self*other
        self.m = Matrix.multiply(self, other)

    def pre_mult_set(self, other):
        # Pre-multiply this matrix with another matrix and store the result in this matrix
        # other*self
        self.m = Matrix.multiply(other, self)

    def post_translate(self, dx, dy, dz):
        # Post-multiply this matrix with a translation matrix
        translation = Matrix()
        translation.set_translate(dx, dy, dz)
        self.post_mult_set(translation)

    def pre_translate(self, dx, dy, dz):
        # Pre-multiply this matrix with a translation matrix
        translation = Matrix()
        translation.set_translate(dx, dy, dz)
        self.pre_mult_set(translation)

    def post_scale(self, sx, sy, sz):
        # Post-multiply this matrix with a scale matrix
        scale = Matrix()
        scale.set_scale(sx, sy, sz)
        self.post_mult_set(scale)

    def pre_scale(self, sx, sy, sz):
        # Pre-multiply this matrix with a scale matrix
        scale = Matrix()
        scale.set_scale(sx, sy, sz)
        self.pre_mult_set(scale)

    def post_rotate(self, angle, vec):
        # Post-multiply this matrix with a rotation matrix
        rotation = Matrix()
        rotation.set_rotate(angle, vec)
        self.post_mult_set(rotation)

    def pre_rotate(self, angle, vec):
        # Pre-multiply this matrix with a rotation matrix
        rotation = Matrix()
        rotation.set_rotate(angle, vec)
        self.pre_mult_set(rotation)

    def affine_mult_point(self, point):
        # Multiply the matrix by a point (affine transformation)
        x, y, z = point.x, point.y, point.z
        transformed_x = self.m[0] * x + self.m[4] * y + self.m[8] * z + self.m[12]
        transformed_y = self.m[1] * x + self.m[5] * y + self.m[9] * z + self.m[13]
        transformed_z = self.m[2] * x + self.m[6] * y + self.m[10] * z + self.m[14]
        return Point3(transformed_x, transformed_y, transformed_z)

    def affine_mult_vector(self, vector):
        # Multiply the matrix by a vector (ignoring translation components)
        dx, dy, dz = vector.dx, vector.dy, vector.dz
        transformed_dx = self.m[0] * dx + self.m[4] * dy + self.m[8] * dz
        transformed_dy = self.m[1] * dx + self.m[5] * dy + self.m[9] * dz
        transformed_dz = self.m[2] * dx + self.m[6] * dy + self.m[10] * dz
        return Vector3(transformed_dx, transformed_dy, transformed_dz)

    def affine_transpose_mult_vector(self, vector):
        # Multiply the matrix by a vector (ignoring translation components)
        dx, dy, dz = vector.dx, vector.dy, vector.dz
        transformed_dx = self.m[0] * dx + self.m[1] * dy + self.m[2] * dz
        transformed_dy = self.m[4] * dx + self.m[5] * dy + self.m[6] * dz
        transformed_dz = self.m[8] * dx + self.m[9] * dy + self.m[10] * dz
        return Vector3(transformed_dx, transformed_dy, transformed_dz)

    def __str__(self):
        # Nicely format the matrix for debugging
        rows = [
            self.m[0:4],
            self.m[4:8],
            self.m[8:12],
            self.m[12:16]
        ]
        return "\n".join(" ".join(f"{val:.2f}" for val in row) for row in rows)
