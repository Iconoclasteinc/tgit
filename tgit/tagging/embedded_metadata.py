# -*- coding: utf-8 -*-
from tgit.tagging.id3_container import ID3Container


def load(filename):
    return ID3Container().load(filename)