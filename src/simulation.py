from __future__ import annotations

import typing
import weakref

from utils.utility import Singleton
from graphics.manager import Manager, Config
from physics.universe import Universe

if typing.TYPE_CHECKING:
    from typing import Callable


@Singleton
class Simulation:
    """
    Global access point to simulation parameters and lifecycle
    """

    g_instance = None

    def __init__(self):
        self._manager = Manager(Config())
        self._universe = Universe()

    @property
    def manager(self):
        return self._manager

    def start(self, preinit : Callable = None):
        if preinit:
            preinit()

        while True:
            self.tick(0.01)
            self._manager.update()

    def tick(self, delta_time : float = 0):
        if delta_time <= 0:
            return
        self._universe.tick(delta_time)
