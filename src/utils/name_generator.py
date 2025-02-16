from __future__ import annotations

import typing
import random


if typing.TYPE_CHECKING:
    from physics.kinetic import Asteroid


NAMES = [
    "Hermes",
    "Ikarus",
    "placeholder"
]


def general_name(asteroid : Asteroid) -> str:
    max_mass = asteroid.MASS[1]
    if asteroid.mass >= max_mass * 0.65:
        return legendary_name(asteroid)

    return f"AST. {int(asteroid.mass / 1e12)}-{int(asteroid.astro_radius / 1e3)}"

def legendary_name(asteroid : Asteroid) -> str:
    return f"{int(asteroid.mass / 1e15)} {NAMES[random.randrange(0, len(NAMES))]}"
