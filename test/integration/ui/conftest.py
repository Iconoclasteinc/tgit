# -*- coding: utf-8 -*-
import pytest

from cute.animatron import Animatron
from cute.prober import EventProcessingProber
from cute.robot import Robot


@pytest.fixture()
def prober():
    return EventProcessingProber()


@pytest.fixture()
def automaton():
    return Animatron()


@pytest.fixture()
def robot():
    return Robot()


@pytest.fixture()
def animaton():
    return Animatron()
