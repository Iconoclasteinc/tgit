# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element

import pytest


@pytest.fixture
def root():
    return Element("root")
