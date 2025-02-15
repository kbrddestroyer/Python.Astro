import random
from venv import create

from physics import kinetic
from physics import universe_utils
from physics.universe_utils import astro_to_gui_distance
from utils.vector import Vector


def initialize():
    sun_r = astro_to_gui_distance(6.96e5)
    sun = kinetic.Kinetic(1.989e30, (255, 255, 255), (500, 500), sun_r * 1000, 0)

    earth_pos = Vector(500, 500).normalized * universe_utils.astro_to_gui_distance(1.49597e11)

    earth = kinetic.Kinetic(5.97e24, (255, 255, 255), (earth_pos.x, earth_pos.y), 2, 1)
    earth.apply_velocity(universe_utils.generate_v1(earth, sun))

    moon = kinetic.Kinetic(7.36e2, (255, 255, 255), (earth_pos.x, earth_pos.y - 5), 1, 1)
    moon.apply_velocity(universe_utils.generate_moon_v1(moon, earth, sun))
