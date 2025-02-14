from __future__ import annotations

from typing import override
from copy import copy

import pygame

from simulation import Simulation
from graphics.manager import Manager
from astro.basics import Object
from utils.vector import Vector

from .universe import Universe


class AstroObject(Object):
    def __init__(self, *args):
        super().__init__()
        self.simulation = Simulation()
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

        self.__simulation = Simulation()
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


class Kinetic(AstroObject):
    def __init__(self, mass, *args):
        super().__init__(*args)
        self._universe = Universe()
        self.mass = mass

        self.current_acceleration = Vector(0, 0)
        self.current_velocity = Vector(0, 0)

        self._universe.register(self)
        self.trace = Trace(500, self.center)

    def on_destroy(self):
        Manager().unregister(self.trace)
        Manager().unregister(self)

    @property
    def acceleration(self):
        return self.current_acceleration

    @property
    def force(self):
        return self.current_acceleration * self.mass

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
        self.position = self.position + self.current_velocity * delta_time

    def calculate_leapfrog(self, delta_time : float):
        self.current_velocity += self.current_acceleration * delta_time

    @override
    def tick(self, delta_time : float):
        self.trace.position = self.center

        self.current_acceleration = Vector(0, 0)
