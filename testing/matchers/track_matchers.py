# -*- coding: utf-8 -*-
from hamcrest import has_properties


def track_with(**properties):
    return has_properties(**properties)
