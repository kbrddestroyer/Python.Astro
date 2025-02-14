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
    fill : Color = (0, 0, 0)


@Singleton
class Manager(object):
    def __init__(self, config):
        self.__config = config

        pygame.init()
        self.__screen = pygame.display.set_mode(config.wnd_size)

    @property
    def screen(self):
        return screen

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.__screen.fill(self.__config.fill)

