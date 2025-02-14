from abc import abstractmethod
from graphics.manager import Manager


class Object:
    def __init__(self):
        manager = Manager()
        manager.register(self)

    @abstractmethod
    def tick(self, delta_time : float):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError
