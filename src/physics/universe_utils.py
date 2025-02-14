from __future__ import annotations

import math
import typing


from utils.vector import Vector

if typing.TYPE_CHECKING:
    from utils.vector import Vector
    from physics.kinetic import Kinetic


G_CONST = 6.6743


def generate_v1(k1 : Kinetic, k2 : Kinetic) -> Vector:
    dist = distance(k1, k2)
    vel = (G_CONST * k2.mass / dist) ** 0.5
    vec = calculate_vector(k1.position, k2.position).normalized.rotate(- math.pi / 2)
    return vec * vel


def distance(k1 : Kinetic, k2 : Kinetic) -> float:
    return math.sqrt((k1.position.x - k2.position.x) ** 2 + (k1.position.y - k2.position.y) ** 2)


def calculate_newtonian(k1 : Kinetic, k2 : Kinetic) -> float:
    dist = distance(k1, k2)
    return G_CONST * k1.mass * k2.mass / (dist ** 2)


def calculate_vector(source : Vector, dest : Vector) -> Vector:
    return Vector(dest.x - source.x, dest.y - source.y)
