from physics import kinetic
from physics import universe_utils
from utils.vector import Vector


def initialize():
    kinetic.AsteroidSpawner()
    sun_r = 6.96e5
    base_point = Vector(820 * universe_utils.UNIT_SIZE, 540 * universe_utils.UNIT_SIZE)

    sun = kinetic.Kinetic(
     1.989e30,
     base_point,
     (255, 255, 255),
     sun_r,
     0
    )

    mercury_pos = base_point + Vector(1, 0).normalized * 5.791e7
    mersury = kinetic.Kinetic(3.33e23, mercury_pos, (255, 0, 0), 2439, 0)
    mersury.apply_velocity(universe_utils.generate_v1(mersury, sun))

    earth_pos = Vector(820 * universe_utils.UNIT_SIZE, 540 * universe_utils.UNIT_SIZE) + Vector(1, 0) * 1.49597e11

    earth = kinetic.Kinetic(5.97e24, Vector(earth_pos.x, earth_pos.y), (255, 255, 255), 6378, 1)
    earth.apply_velocity(universe_utils.generate_v1(earth, sun))
