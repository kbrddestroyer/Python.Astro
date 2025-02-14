from __future__ import annotations

import typing

from utils.utility import Singleton
from graphics.manager import Manager, Config

if typing.TYPE_CHECKING:
    pass


@Singleton
class Simulation:
    """
    Global access point to simulation parameters and lifecycle
    """

    g_instance = None

    def __init__(self):
        self._manager = Manager(Config())

    def start(self):
        while True:
            self.tick()
            self._manager.update()

    def tick(self, delta_time : float = 0):
        pass
