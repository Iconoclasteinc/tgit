# -*- coding: utf-8 -*-
import os


def path(filepath, *more):
    filename = os.path.join(os.path.dirname(__file__), filepath)
    for filepath in more:
        filename = os.path.join(filename, filepath)

    return os.path.abspath(filename)
