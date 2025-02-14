from __future__ import annotations

import typing

from utils.utility import Singleton
from graphics.manager import Manager
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
        self.__running = True

        self._manager = Manager()
        self._universe = Universe()

    @property
    def manager(self):
        return self._manager

    def finalize(self):
        self.__running = False
        del self._universe
        del self._manager

    def start(self, init : Callable = None):
        if init:
            init()

        while self.__running:
            self.tick(0.1)
            self._manager.update()

    def tick(self, delta_time : float = 0):
        if delta_time <= 0:
            return
        self._universe.tick(delta_time)
