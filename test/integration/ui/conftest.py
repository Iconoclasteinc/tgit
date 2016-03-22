# -*- coding: utf-8 -*-
import pytest

from cute.animatron import Animatron
from cute.prober import EventProcessingProber


@pytest.fixture()
def prober():
    return EventProcessingProber()


# The animatron requires a running qt event loop
@pytest.fixture()
def automaton(qt):
    return Animatron()
