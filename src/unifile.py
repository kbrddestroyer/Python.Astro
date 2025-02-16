from physics import kinetic
from physics import universe_utils
from utils.vector import Vector


def initialize():
    kinetic.Spawner(kinetic.Asteroid, 0.5)
    sun_r = 6.96e5
    base_point = Vector(820 * universe_utils.UNIT_SIZE, 540 * universe_utils.UNIT_SIZE)

    sun = kinetic.Kinetic(
        1.989e30,
        base_point,
        (255, 255, 255),
        sun_r,
        0,
        "Sun"
    )

    mercury_pos = base_point + Vector(1, 0).normalized * 5.791e7
    mercury = kinetic.Kinetic(3.33e23, mercury_pos, (255, 0, 0), 2439, 0, 'Mercury')
    mercury.apply_velocity(universe_utils.generate_v1(mercury, sun))

    venus_pos = base_point + Vector(1, 0).normalized * 1.08e8
    venus = kinetic.Kinetic(4.8675e24, venus_pos, (255, 255, 255), 6051, 0, 'Venus')
    venus.apply_velocity(universe_utils.generate_v1(venus, sun))

    earth_pos = base_point + Vector(1, 0) * 1.49597e8
    earth = kinetic.Kinetic(5.97e24, earth_pos, (255, 255, 255), 6378, 1, 'Earth')
    earth.apply_velocity(universe_utils.generate_v1(earth, sun))

    mars_pos = base_point + Vector(1, 0) * 2.06e8
    mars = kinetic.Kinetic(6.4171e23, mars_pos, (255, 255, 255), 3396, 1, 'Mars')
    mars.apply_velocity(universe_utils.generate_v1(mars, sun))

    jupiter_pos = base_point + Vector(1, 0) * 7.40e8
    jupiter = kinetic.Kinetic(1.8986e27, jupiter_pos, (255, 255, 255), 69911, 1, 'Jupiter')
    jupiter.apply_velocity(universe_utils.generate_v1(jupiter, sun))

    saturn_pos = base_point + Vector(1, 0) * 1.25e9
    saturn = kinetic.Kinetic(1.8986e27, saturn_pos, (255, 255, 255), 69911, 1, 'Saturn')
    saturn.apply_velocity(universe_utils.generate_v1(saturn, sun))
