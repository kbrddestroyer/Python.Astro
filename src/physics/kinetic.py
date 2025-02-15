from __future__ import annotations

import math
from typing import override, Tuple
from copy import copy
import random

import pygame
import simulation

from graphics.manager import Manager
from astro.basics import Object
from utils.vector import Vector
from . import universe
from .universe_utils import UNIT_SIZE, astro_to_gui_distance


class AstroObject(Object):
    def __init__(self):
        super().__init__()
        universe.Universe().register(self)

    def on_destroy(self):
        pass

    @override
    def tick(self, delta_time : float):
        pass

    @override
    def render(self):
        pass


class AsteroidSpawner(AstroObject):
    CHANCE = 100

    def __init__(self):
        self.counter = 0
        super().__init__()

    @override
    def tick(self, delta_time : float):
        self.counter += delta_time

        if self.counter < 10e5:
            return

        self.counter = 0

        chance = random.random()

        if chance < (self.CHANCE / 100):
            Asteroid()


class AstroKineticObject(AstroObject):
    def __init__(self, *args):
        super().__init__()
        self.simulation = simulation.Simulation()
        self.color, self.center, self.radius, self.width = args

    def move(self, position):
        self.center = position

    @property
    def position(self):
        return Vector(*self.center)

    @position.setter
    def position(self, value : Vector):
        self.center = (value.x, value.y)

    @override
    def tick(self, delta_time : float):
        pass

    @override
    def render(self):
        pygame.draw.circle(
            self.simulation.manager.screen,
            self.color,
            self.center,
            self.radius,
            self.width
        )


class Trace(Object):
    def __init__(self, length, start_position):
        super().__init__()

        self.__simulation = simulation.Simulation()
        self.__trace = []
        self.__length = length
        self.__position = copy(start_position)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        if len(self.__trace) >= self.__length:
            self.__trace.pop(0)
        self.__trace.append(copy(self.__position))

        self.__position = position

    @override
    def tick(self, delta_time : float):
        pass

    @override
    def render(self):
        for pos_id in range(1, len(self.__trace)):
            start = self.__trace[pos_id]
            end = self.__trace[pos_id - 1]

            pygame.draw.line(
                self.__simulation.manager.screen,
                (
                125 - int((len(self.__trace) - pos_id) / len(self.__trace) * 125),
                125 - int((len(self.__trace) - pos_id) / len(self.__trace) * 125),
                125 - int((len(self.__trace) - pos_id) / len(self.__trace) * 125)
            ), start, end, 2)


class Kinetic(AstroKineticObject):
    def __init__(self, mass, *args):
        super().__init__(*args)
        self.mass = mass

        self.current_acceleration = Vector(0, 0)
        self.current_velocity = Vector(0, 0)
        self.trace = Trace(500, self.center)

    @staticmethod
    def astro_to_gui_pos(astro_pos : Vector) -> Tuple[int, int]:
        return astro_pos.normalized * astro_to_gui_distance(astro_pos.magnitude)

    @override
    def on_destroy(self):
        Manager().unregister(self.trace)
        Manager().unregister(self)

    @property
    def acceleration(self):
        return self.current_acceleration

    @property
    def force(self):
        return self.current_acceleration * self.mass

    def set_position(self, position : Vector):
        center = Kinetic.astro_to_gui_pos(position)
        self.astro_pos = position
        self.center = center

    def apply_force(self, force : Vector):
        self.current_acceleration = force / self.mass

    def apply_acceleration(self, acceleration : Vector):
        self.current_acceleration = acceleration

    def apply_velocity(self, velocity : Vector):
        self.current_velocity = velocity

    def accelerate(self, acceleration : Vector):
        self.current_acceleration += acceleration

    def precalculate_leapfrog(self, delta_time : float):
        self.current_velocity += self.current_acceleration * 0.5 * delta_time
        self.position = self.position + (self.current_velocity * delta_time) / UNIT_SIZE

    def calculate_leapfrog(self, delta_time : float):
        self.current_velocity += self.current_acceleration * delta_time

    @override
    def tick(self, delta_time : float):
        self.trace.position = self.center

        self.current_acceleration = Vector(0, 0)


class Asteroid(Kinetic):
    MASS = (1, 1.e17)
    POSITION = (10, 1600, 10, 1000)
    BASE_VELOCITY_MUL = 100000
    DENSITY = 2.6
    BASE_RADIUS_MUL = 1000

    @staticmethod
    def radius(mass):
        return ( 3 * Asteroid.DENSITY * mass / 4 * math.pi ) ** ( 1 / 3 ) * Asteroid.BASE_RADIUS_MUL

    @staticmethod
    def generate(bounds):
        return random.random() * (bounds[1] - bounds[0]) + bounds[0]

    def __init__(self):
        mass = self.generate(self.MASS)
        pos_x = self.generate(self.POSITION[:2])
        pos_y = self.generate(self.POSITION[2:])
        rad = astro_to_gui_distance(self.radius(mass))
        super().__init__(mass, (255, 255, 255), (pos_x, pos_y), rad, 1)

        velocity = self.generate((-1, 1)) * self.BASE_VELOCITY_MUL
        vector = Vector(1, 0).rotate(self.generate((0, 2 * math.pi))).normalized

        self.apply_velocity(vector * velocity)
