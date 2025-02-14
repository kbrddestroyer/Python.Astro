from physics import kinetic
from physics import universe_utils


def initialize():
    sun = kinetic.Kinetic(10000, (255, 255, 255), (500, 500), 50, 0)
    planet = kinetic.Kinetic(1.496, (255, 255, 255), (550, 300), 5, 0)

    planet.apply_velocity(universe_utils.generate_v1(planet, sun))
