from __future__ import annotations

import math
import typing

from graphics.manager import Manager
from utils.utility import Singleton
from utils.vector import Vector

from . import universe_utils


if typing.TYPE_CHECKING:
    from kinetic import Kinetic


@Singleton
class Universe:
    def __init__(self):
        self.__registry = []
        self.__remove_queue = []

    def register(self, kinetic : Kinetic):
        assert kinetic not in self.__registry
        self.__registry.append(kinetic)

    def unregister(self, kinetic):
        if kinetic not in self.__registry:
            return
        if kinetic in self.__remove_queue:
            return
        self.__remove_queue.append(kinetic)
        kinetic.onDestroy()

    def try_collapse(self, k1 : Kinetic, k2 : Kinetic):
        dist = universe_utils.distance(k1, k2)
        if (k1.radius + k2.radius) < dist:
            return

        if k2.radius > k1.radius:
            k1, k2 = k2, k1

        self.__collapse_kinetics(k1, k2)

    def __collapse_kinetics(self, k1: Kinetic, k2 : Kinetic):
        k1.currentForce = Vector.vector_sum(k1.currentForce, k2.currentForce)
        dist = universe_utils.distance(k1, k2)

        position = k1.position + (k1.position - k2.position) / (k1.radius + k2.radius)
        k1.center = (position.x, position.y)

        k1.radius = math.sqrt(k1.radius ** 2 + k2.radius ** 2)
        k1.mass += k2.mass
        self.unregister(k2)

    def tick(self, delta_time : float = 0):
        for kinetic in self.__remove_queue:
            self.__registry.remove(kinetic)

        self.__remove_queue.clear()

        self.__tick(delta_time)

    def __tick(self, delta_time : float = 0):
        for kinetic in self.__remove_queue:
            self.__registry.pop(kinetic)
            Manager().unregister(kinetic)

        self.__remove_queue.clear()

        for kinetic in self.__registry:
            for other in self.__registry:
                if other is kinetic:
                    continue

                vec = universe_utils.calculate_vector(kinetic.position, other.position)
                f = universe_utils.calculate_newtonian(kinetic, other)

                kinetic.currentForce = Vector.vector_sum(kinetic.currentForce, vec * f)

                self.try_collapse(kinetic, other)
            kinetic.tick(delta_time)

