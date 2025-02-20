"""
TDD is good. Make some unit tests. Sometimes it's fun, sometimes not, but anyway TDD is awesome.
Respect others, never change unit tests without a reason (for example to bypass status checks).
"""

import pytest

from physics import universe, kinetic, universe_utils
from utils.utility import Singleton
from utils.vector import Vector
from graphics import manager


@Singleton
class FakeManager:
    def __init__(self):
        self.__render_queue = []
        self.__remove_queue = []

    def register(self, obj):
        if obj not in self.__render_queue:
            self.__render_queue.append(obj)

    def unregister(self, obj):
        if obj in self.__render_queue and obj not in self.__remove_queue:
            self.__remove_queue.append(obj)

    def update(self):
        pass

    @property
    def screen(self):
        return None

    @staticmethod
    def set_caption(cap : str):
        pass


@pytest.fixture()
def fake_manager(monkeypatch):
    monkeypatch.setattr(manager.Manager, "_instance", FakeManager())


@pytest.fixture()
def no_sanitize(monkeypatch):
    uni = universe.Universe()
    monkeypatch.setattr(uni, "_Universe__sanitize", lambda _: None)


def test_kinetic_tick(monkeypatch, fake_manager, no_sanitize):
    dummy = kinetic.Kinetic(
        100, Vector(0, 0), (255, 255, 255), 1, 1, "Test Dummy"
    )
    monkeypatch.setattr(dummy, "try_scatter", lambda: False)

    uni = universe.Universe()
    assert uni.kinetic_registry.registered(dummy)
    assert len(uni.kinetic_registry) == 1
    uni.tick(0.1)

    assert dummy.astro_position == Vector(0, 0)
    dummy.apply_velocity(Vector(2, 0))
    uni.tick(1)
    assert dummy.astro_position == Vector(2, 0)
    uni.tick(1)
    assert dummy.astro_position == Vector(4, 0)

    dummy.astro_position = Vector(0, 0)
    dummy.apply_velocity(Vector(0, 0))
    dummy.apply_acceleration(Vector(2, 0))
    uni.tick(0.1)
    assert not dummy.current_acceleration.magnitude

    dummy.apply_force(Vector(1, 0))
    assert dummy.current_acceleration.magnitude == 1 / dummy.mass
    uni.tick(0.1)
    assert dummy.current_acceleration.magnitude == 0
    assert dummy.current_velocity.magnitude
    uni.finalize()


def test_physics_kinetic_scatter(monkeypatch, fake_manager, no_sanitize):
    # Well, it's mostly done to sanitize the universe and prevent FPS loss
    # Kinetic will scatter, when outside forces apply acceleration,
    # that's 30 times bigger that it's surface acceleration of gravity

    dummy = kinetic.Kinetic(
        1e15, Vector(0, 0), (255, 255, 255), 500, 1, "Test Dummy"
    )

    uni = universe.Universe()

    registry = uni.kinetic_registry
    assert len(registry) == 1

    dummy.apply_acceleration(Vector(2, 0))
    uni.tick(1)
    assert len(registry) == 1

    dummy.apply_acceleration(Vector(dummy.mass / 250000 * universe_utils.G_CONST * 30, 0.1))
    uni.tick(1)
    assert len(registry) == 4
    uni.finalize()


@pytest.mark.parametrize(
    'initial_velocity',
    [
        101,
        250,
        500,
        1000,
        1e6
    ]
)
def test_physics_improved_impacts(monkeypatch, fake_manager, no_sanitize, initial_velocity):
    uni = universe.Universe()

    dummy1 = kinetic.Kinetic(
        2, Vector(0, 0), (255, 255, 255), 5, 1, "Test Dummy 1"
    )
    dummy2 = kinetic.Kinetic(
        2, Vector(100, 0), (255, 255, 255), 5, 1, "Test Dummy 2"
    )
    registry = uni.kinetic_registry
    assert len(registry) == 2

    dummy1.apply_velocity(Vector(initial_velocity, 0))
    assert uni.try_collapse(dummy1, dummy2, 1)
    uni.tick(0.1)
    assert len(registry) == 1
    uni.finalize()

@pytest.mark.parametrize(
    'initial_velocity',
    [
        101,
        250,
        500,
        1000,
        1e6
    ]
)
def test_physics_improved_impacts_non_direct(monkeypatch, fake_manager, no_sanitize, initial_velocity):
    # Well, in fact those object won't actually collide
    # That will be indirect impact, so instead they will break into fragments.
    # This simulation is simplified, so we'll take it as collision and collapse two objects into one
    #
    # I've had a bunch of bugs with this algo, so here's the test

    uni = universe.Universe()

    dummy1 = kinetic.Kinetic(
        2, Vector(0, 5), (255, 255, 255), 5, 1, "Test Dummy 1"
    )
    dummy2 = kinetic.Kinetic(
        2, Vector(100, -5), (255, 255, 255), 5, 1, "Test Dummy 2"
    )
    registry = uni.kinetic_registry
    assert len(registry) == 2

    dummy1.apply_velocity(Vector(initial_velocity, 0))
    assert uni.try_collapse(dummy1, dummy2, 1)
    uni.tick(0.1)
    assert len(registry) == 1
    uni.finalize()
