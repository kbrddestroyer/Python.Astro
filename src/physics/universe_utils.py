from __future__ import annotations

import math
import typing


from utils.vector import Vector

if typing.TYPE_CHECKING:
    from utils.vector import Vector
    from physics.kinetic import Kinetic


G_CONST = 6.6743


def distance(astro1 : Kinetic, astro2 : Kinetic) -> float:
    return math.sqrt((astro1.position.x - astro2.position.x) ** 2 + (astro1.position.y - astro2.position.y) ** 2)


def calculate_newtonian(astro1, astro2) -> float:
    dist = distance(astro1, astro2)
    return G_CONST * astro1.mass * astro2.mass / (dist ** 2)


def calculate_vector(source : Vector, dest : Vector) -> Vector:
    return Vector(dest.x - source.x, dest.y - source.y)
