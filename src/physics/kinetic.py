from __future__ import annotations

from dataclasses import dataclass

import pygame
import typing

from typing import override

from simulation import Simulation
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


class Kinetic(AstroObject):
    def __init__(self, mass, *args):
        super(Kinetic, self).__init__(*args)
        self._universe = Universe()
        self.mass = mass
        self.currentForce = Vector(0, 0)
        self._universe.register(self)

    def __del__(self):
        if self._universe:
            self._universe.unregister(self)

    @override
    def tick(self, delta_time : float):
        a = self.currentForce / self.mass
        r = (a * (delta_time ** 2)) / 2
        desired = (r.x + self.center[0], r.y + self.center[1])
        self.center = desired
