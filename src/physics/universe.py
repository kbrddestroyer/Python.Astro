from __future__ import annotations

import math
import typing

from physics import kinetic
from graphics import manager
from utils.utility import Singleton
from utils.vector import Vector

from . import universe_utils

if typing.TYPE_CHECKING:
    from kinetic import Kinetic, AstroObject


class Registry:
    def __init__(self):
        self.__registry = []
        self.__remove_queue = []

        self.__index = 0

    @property
    def registry(self):
        return self.__registry

    def __iter__(self):
        for item in self.__registry:
            yield item

    def __len__(self):
        return len(self.__registry)

    def register(self, obj : AstroObject):
        if obj in self.__registry:
            return
        self.__registry.append(obj)

    def unregister(self, obj : AstroObject):
        if obj not in self.__registry or obj in self.__remove_queue:
            return
        self.__remove_queue.append(obj)
        obj.on_destroy()

    def update(self):
        for obj in self.__remove_queue:
            self.__registry.remove(obj)

        self.__remove_queue.clear()

@Singleton
class Universe:
    def __init__(self):
        self.kinetic_registry = Registry()
        self.global_registry = Registry()

    def register(self, obj : AstroObject):
        if isinstance(obj, kinetic.AstroKineticObject):
            self.kinetic_registry.register(obj)
        else:
            self.global_registry.register(obj)

    def unregister(self, obj : AstroObject):
        if isinstance(obj, kinetic.AstroKineticObject):
            self.kinetic_registry.unregister(obj)
        else:
            self.global_registry.register(obj)

    def try_collapse(self, k1 : Kinetic, k2 : Kinetic) -> bool:
        dist = universe_utils.distance(k1, k2)
        if (k1.astro_radius + k2.astro_radius) < dist:
            return False

        if k2.astro_radius > k1.astro_radius:
            k1, k2 = k2, k1

        self.__collapse_kinetics(k1, k2)
        return True

    def __sanitize(self, k : Kinetic):
        center = Vector(*manager.Config.WND_SIZE) / 2
        dist = math.sqrt((k.position.x - center.x) ** 2 + (k.position.y - center.y) ** 2)

        if dist > max(center.x, center.y):
            self.unregister(k)

    def __collapse_kinetics(self, k1: Kinetic, k2 : Kinetic):
        k1.apply_force(Vector.vector_sum(k1.force, k2.force))
        position = k1.astro_position + (k1.astro_position - k2.astro_position) / (k1.astro_radius + k2.astro_radius)
        k1.astro_position = position

        k1.astro_radius = math.sqrt(k1.astro_radius ** 2 + k2.astro_radius ** 2)
        k1.mass += k2.mass
        self.unregister(k2)

    def tick(self, delta_time : float = 0):
        self.kinetic_registry.update()
        self.__tick(delta_time)

    def __tick(self, delta_time : float = 0):
        for obj in self.kinetic_registry:
            self.__sanitize(obj)

            obj.precalculate_leapfrog(delta_time)
            for other in self.kinetic_registry:
                if other is obj:
                    continue

                if self.try_collapse(obj, other):
                    continue

                vec = universe_utils.calculate_vector(obj.astro_position, other.astro_position)
                f = universe_utils.calculate_newtonian(obj, other)

                obj.apply_force(Vector.vector_sum(obj.force, vec.normalized * f))

            obj.calculate_leapfrog(delta_time)
            obj.tick(delta_time)

        for glob_obj in self.global_registry:
            glob_obj.tick(delta_time)

        manager.Manager().set_caption(f"Astro Simulation | simulating {len(self.kinetic_registry)} kinetics")
