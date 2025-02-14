import random
from venv import create

from physics import kinetic
from physics import universe_utils


def initialize():
    sun = kinetic.Kinetic(100, (255, 255, 255), (500, 500), 10, 0)

    def create_planetary_system(pos, moons):
        planet = kinetic.Kinetic(1.6, (255, 255, 255), pos, 5, 1)

        def generate_moon(moon, p, s):
            vel1 = universe_utils.generate_v1(moon, p)
            vel2 = universe_utils.generate_v1(moon, s)
            return vel1 + vel2

        planet.apply_velocity(universe_utils.generate_v1(planet, sun))

        for _ in range(moons):
            m_pos = (
                pos[0] + random.randint(0, 30),
                pos[1] + random.randint(0, 30)
            )

            moon = kinetic.Kinetic(4.96e-11, (255, 255, 255), m_pos, 1, 0)
            moon.apply_velocity(generate_moon(moon, planet, sun))

    create_planetary_system((900, 300), 3)

    planet = kinetic.Kinetic(1.6, (255, 255, 255), (400, 500), 3, 1)
    planet.apply_velocity(universe_utils.generate_v1(planet, sun))


    planet = kinetic.Kinetic(2.6, (255, 255, 255), (700, 20), 10, 1)
    planet.apply_velocity(universe_utils.generate_v1(planet, sun))