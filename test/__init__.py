# -*- coding: utf-8 -*-
from hamcrest import match_equality as matching, has_property, contains


def exception_with_message(message):
    return matching(has_args_containing(message))


def has_args_containing(message):
    return has_property("args", contains(message))
