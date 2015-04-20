# -*- coding: utf-8 -*-
from tgit.metadata import Metadata
from tgit.tagging.id3_container import ID3Container


class FlacContainer(object):
    def load(self, filename):
        return { 'leadPerformer': "Joell Miller" }


containers = {
    '.mp3': ID3Container(),
    '.flac': FlacContainer()
}


def load(filename):
    for key, value in containers.items():
        if filename.endswith(key):
            return value.load(filename)

    return Metadata()