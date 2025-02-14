from __future__ import annotations

from dataclasses import dataclass

import pygame
import typing

from copy import copy

from typing import override

from simulation import Simulation
from graphics.manager import Manager
from astro.basics import Object
from utils.vector import Vector

from .universe import Universe


class AstroObject(Object):
    def __init__(self, *args):
        super(AstroObject, self).__init__()
        self.simulation = Simulation()
        self.color, self.center, self.radius, self.width = args

    def move(self, position):
        self.center = position

    @property
    def position(self):
        return Vector(*self.center)

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
        super(Trace, self).__init__()

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
        for posID in range(1, len(self.__trace)):
            start = self.__trace[posID]
            end = self.__trace[posID - 1]

            pygame.draw.line(
                self.__simulation.manager.screen,
                (
                125 - int((len(self.__trace) - posID) / len(self.__trace) * 125),
                125 - int((len(self.__trace) - posID) / len(self.__trace) * 125),
                125 - int((len(self.__trace) - posID) / len(self.__trace) * 125)
            ), start, end, 2)


class Kinetic(AstroObject):
    def __init__(self, mass, *args):
        super(Kinetic, self).__init__(*args)
        self._universe = Universe()
        self.mass = mass
        self.currentForce = Vector(0, 0)
        self._universe.register(self)

        self.trace = Trace(5000, self.center)

    def onDestroy(self):
        Manager().unregister(self.trace)
        Manager().unregister(self)

    @override
    def tick(self, delta_time : float):
        a = self.currentForce / self.mass
        r = (a * (delta_time ** 2)) / 2
        desired = (r.x + self.center[0], r.y + self.center[1])
        self.center = desired
        self.trace.position = self.center
