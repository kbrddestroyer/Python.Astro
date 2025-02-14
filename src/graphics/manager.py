"""
Simple window managing using pygame

Implemented features:
- window creation and handling window events
"""

from __future__ import annotations

import sys
import typing
from dataclasses import dataclass

import pygame
from utils.utility import Singleton


if typing.TYPE_CHECKING:
    from typing import Tuple
    from pygame import Color


@dataclass
class Config:
    wnd_size : Tuple[int, int] = (640, 480)
    fill : Color = (10, 10, 10)


@Singleton
class Manager(object):
    def __init__(self, config):
        self.__config = config

        pygame.init()
        self.__screen = pygame.display.set_mode(config.wnd_size)

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
                sys.exit()

        self.__screen.fill(self.__config.fill)
        self.__render()
        pygame.display.flip()
