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

    @property
    def registry(self):
        return self.__registry

    def __iter__(self):
        yield from self.__registry

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

    def registered(self, obj):
        return obj in self.__registry and obj not in self.__remove_queue

    def update(self):
        for obj in self.__remove_queue:
            self.__registry.remove(obj)

        self.__remove_queue.clear()


@Singleton
class UniverseLogger:
    def __init__(self):
        self.__log = []

    def on_registered(self, k: Kinetic):
        self.__log.append(f"{k.name} is created in universe!")

    def on_unregistered(self, k: Kinetic):
        self.__log.append(f"{k.name} is gone now!")

    def on_collapse(self, k1: Kinetic, k2: Kinetic):
        self.__log.append(f"{k2.name} impacted {k1.name}, becoming a part of it!")

    def on_throttle(self, k: Kinetic, v: Vector):
        self.__log.append(f"{k.name} throttled by {v.magnitude / (k.current_velocity.magnitude + 1)}!")

    def finalize(self):
        with open('universe.log', 'w') as f:
            for log in self.__log:
                f.write(log + "\n")


@Singleton
class Universe:
    def __init__(self):
        self.kinetic_registry = Registry()
        self.global_registry = Registry()

    def finalize(self):
        UniverseLogger().finalize()

    def register(self, obj : AstroObject):
        if isinstance(obj, kinetic.AstroKineticObject):
            self.kinetic_registry.register(obj)
            UniverseLogger().on_registered(obj)
        else:
            self.global_registry.register(obj)

    def unregister(self, obj : AstroObject):
        if isinstance(obj, kinetic.AstroKineticObject):
            self.kinetic_registry.unregister(obj)
            UniverseLogger().on_unregistered(obj)
        else:
            self.global_registry.unregister(obj)

    def try_collapse(self, k1 : Kinetic, k2 : Kinetic) -> bool:
        dist = universe_utils.distance(k1, k2)
        if (k1.astro_radius + k2.astro_radius) < dist:
            return False

        if k2.mass > k1.mass:
            k1, k2 = k2, k1

        self.__collapse_kinetics(k1, k2)
        return True

    def __sanitize(self, k : Kinetic):
        center = Vector(*manager.Config.WND_SIZE) / 2
        dist = math.sqrt((k.position.x - center.x) ** 2 + (k.position.y - center.y) ** 2)

        if dist > max(center.x, center.y):
            self.unregister(k)

    def __collapse_kinetics(self, k1: Kinetic, k2 : Kinetic):
        velocity = (k1.current_velocity * k1.mass + k2.current_velocity * k2.mass) / (k1.mass + k2.mass)
        k1.apply_velocity(velocity)

        position = k1.astro_position + (k1.astro_position - k2.astro_position) / (k1.astro_radius + k2.astro_radius)
        k1.astro_position = position

        k1.astro_radius = math.sqrt(k1.astro_radius ** 2 + k2.astro_radius ** 2)
        k1.mass += k2.mass
        kinetic.ImpactEvent(k1.center, 500)
        UniverseLogger().on_collapse(k1, k2)
        self.unregister(k2)

    def tick(self, delta_time : float = 0):
        self.kinetic_registry.update()
        self.global_registry.update()
        self.__tick(delta_time)

    def __tick(self, delta_time : float = 0):
        for obj in self.kinetic_registry:
            self.__sanitize(obj)
            if not self.kinetic_registry.registered(obj):
                continue
            obj.precalculate_leapfrog(delta_time)
            for other in self.kinetic_registry:
                if other is obj:
                    continue

                if not self.kinetic_registry.registered(other):
                    continue

                if self.try_collapse(obj, other):
                    continue

                vec = universe_utils.calculate_vector(obj.astro_position, other.astro_position)
                f = universe_utils.calculate_newtonian(obj, other)

                obj.apply_force(Vector.vector_sum(obj.force, vec.normalized * f))

            if obj.current_velocity.magnitude < (obj.current_acceleration * delta_time).magnitude:
                UniverseLogger().on_throttle(obj, obj.current_acceleration * delta_time)
            obj.calculate_leapfrog(delta_time)
            obj.tick(delta_time)

        for glob_obj in self.global_registry:
            glob_obj.tick(delta_time)

        manager.Manager().set_caption(f"Astro Simulation | simulating {len(self.kinetic_registry)} kinetics")
