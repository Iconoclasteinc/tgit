# -*- coding: utf-8 -*-
from os.path import exists

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit import tagging
from tgit.metadata import Image
from tgit.util import fs


class AlbumWorkspace(object):
    def __init__(self, local_path):
        self._local_path = local_path

    @property
    def root_path(self):
        return self._local_path.strpath

    def path(self, filename):
        return self._local_path.join(filename).strpath

    def contains_track(self, filename, front_cover=None, **tags):
        if not exists(self.path(filename)):
            raise AssertionError("Track file '{}' not found in workspace".format(filename))

        track = tagging.load_track(self.path(filename))
        images = []
        # todo use builders and metadata
        if front_cover:
            image, desc = front_cover
            mime = fs.guess_mime_type(image)
            images.append(Image(mime, fs.binary_content_of(image), type_=Image.FRONT_COVER, desc=desc))

        assert_that(track.metadata, has_entries(tags), 'metadata tags')
        assert_that(track.metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        self._local_path.remove()
