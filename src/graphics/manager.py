"""
Simple window managing using pygame

Implemented features:
- window creation and handling window events
"""

from __future__ import annotations

import typing
from enum import EnumType

import pygame
import simulation
from utils.utility import Singleton


if typing.TYPE_CHECKING:
    from typing import Tuple
    from pygame import Color


class Config(EnumType):
    WND_SIZE : Tuple[int, int]  = (1640, 1080)
    FILL_COLOR : Color          = (10, 10, 10)


@Singleton
class Manager:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(Config.WND_SIZE)

        self.__render_queue = []
        self.__remove_queue = []

    def register(self, obj):
        if obj not in self.__render_queue:
            self.__render_queue.append(obj)

    def unregister(self, obj):
        if obj in self.__render_queue and obj not in self.__remove_queue:
            self.__remove_queue.append(obj)

    @property
    def screen(self):
        return self.__screen

    def __render(self):
        for obj in self.__remove_queue:
            self.__render_queue.remove(obj)

        self.__remove_queue.clear()

        for obj in self.__render_queue:
            obj.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                simulation.Simulation().finalize()
                return

        self.__screen.fill(Config.FILL_COLOR)
        self.__render()
        pygame.display.flip()
