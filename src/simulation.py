from __future__ import annotations

import typing

from graphics import manager
from physics import universe
from utils.utility import Singleton

from config.config import Configuration

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

        self._manager = manager.Manager()
        self._universe = universe.Universe()

    @property
    def manager(self):
        return self._manager

    def finalize(self):
        self.__running = False
        self._universe.finalize()
        del self._universe
        del self._manager

    def start(self, init : Callable = None):
        if init:
            init()

        while self.__running:
            self.tick(Configuration.DELTA_TIME)
            self._manager.update()

    def tick(self, delta_time : float = 0):
        if delta_time <= 0:
            return
        self._universe.tick(delta_time)
