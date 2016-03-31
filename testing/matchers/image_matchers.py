# -*- coding: utf-8 -*-
from hamcrest import anything
from hamcrest import has_properties


def image_with(mime=anything(), data=anything(), desc=anything(), type_=anything()):
    return has_properties(mime=mime, data=data, desc=desc, type=type_)