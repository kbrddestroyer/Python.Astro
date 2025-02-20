from __future__ import annotations

import typing
import random


if typing.TYPE_CHECKING:
    from physics.kinetic import Asteroid


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

    return f"AST. {int(mass / 1e9)}-{int(radius * 1000)}"


def unique_asteroid_name(mass) -> str:
    return f"{int(mass / 1e9)} {ASTEROIDS[random.randrange(0, len(ASTEROIDS))]}"
