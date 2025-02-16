from __future__ import annotations

import typing
import random


if typing.TYPE_CHECKING:
    from physics.kinetic import Asteroid, Blackhole


ASTEROIDS = [
    "Hermes",
    "Ikarus",
    "Fortuna",
    "Themis",
    "Flora",
    "Metis",
    "Nysa",
    "Doris",
    "Echo",
    "Bravo",
    "Charlie",
    "Freia",
    "Io"
]



def general_asteroid_name(asteroid : Asteroid, mass, radius) -> str:
    max_mass = asteroid.MASS[1]
    if mass >= max_mass * 0.65:
        return unique_asteroid_name(mass)

    return f"AST. {int(mass / 1e12)}-{int(radius / 1e3)}"


def unique_asteroid_name(mass) -> str:
    return f"{int(mass / 1e15)} {ASTEROIDS[random.randrange(0, len(ASTEROIDS))]}"
