from __future__ import annotations

import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __iter__(self):
        return iter([self.x, self.y])

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        raise NotImplementedError

    @staticmethod
    def vector_sum(v1 : Vector, v2 : Vector):
        if v1.magnitude > 0 and v2.magnitude > 0:
            cosines = (v1.x * v2.x + v1.y * v2.y) / (v1.magnitude * v2.magnitude)
            force = math.sqrt(v1.magnitude ** 2 + v2.magnitude ** 2 + 2 * v1.magnitude * v2.magnitude * cosines)
            return (v1 + v2).normalized * force

        return v1 + v2

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self):
        return Vector(self.x / self.magnitude, self.y / self.magnitude)

    def rotate(self, radian):
        x = self.x * math.cos(radian) - self.y * math.sin(radian)
        y = self.x * math.sin(radian) + self.y * math.cos(radian)

        self.x = x
        self.y = y
        return self
