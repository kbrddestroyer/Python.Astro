from __future__ import annotations

import math
import typing


from utils.vector import Vector

if typing.TYPE_CHECKING:
    from physics.kinetic import Kinetic


G_CONST     = 6.6743e-11  # Newtonian gravity constant
UNIT_SIZE   = 3.0e8       # Unit to meter


def generate_v1(k1 : Kinetic, k2 : Kinetic) -> Vector:
    dist = distance(k1, k2)
    vel = (G_CONST * k2.mass / dist) ** 0.5
    vec = calculate_vector(k1.position, k2.position).normalized.rotate(- math.pi / 2)
    return vec * vel


def generate_moon_v1(moon : Kinetic, planet : Kinetic, sun : Kinetic):
    return generate_v1(moon, sun) + generate_v1(moon, planet)


def gui_distance(k1 : Kinetic, k2 : Kinetic):
    return math.sqrt((k1.position.x - k2.position.x) ** 2 + (k1.position.y - k2.position.y) ** 2)


def distance(k1 : Kinetic, k2 : Kinetic) -> float:
    return gui_distance(k1, k2) * UNIT_SIZE


def astro_to_gui_distance(astro_dist : float) -> float:
    return astro_dist / UNIT_SIZE


def calculate_newtonian(k1 : Kinetic, k2 : Kinetic) -> float:
    return G_CONST * k1.mass * k2.mass / (distance(k1, k2) ** 2)


def calculate_vector(source : Vector, dest : Vector) -> Vector:
    return Vector(dest.x - source.x, dest.y - source.y)
