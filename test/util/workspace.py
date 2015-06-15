# -*- coding: utf-8 -*-
import os
import shutil

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit import tagging
from tgit.metadata import Image
from tgit.util import fs


class AlbumWorkspace(object):
    def __init__(self, root):
        self._root = root

    @property
    def root(self):
        return self._root

    def path(self, filename):
        return os.path.join(self._root, filename)

    def contains_track(self, filename, front_cover=None, **tags):
        if not os.path.exists(self.path(filename)):
            raise AssertionError("Track file '{}' not found in workspace".format(filename))

        metadata = tagging.load_metadata(self.path(filename))
        images = []
        # todo use builders and metadata
        if front_cover:
            image, desc = front_cover
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.binary_content_of(image), type_=Image.FRONT_COVER, desc=desc))

        assert_that(metadata, has_entries(tags), 'metadata tags')
        assert_that(metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        shutil.rmtree(self._root)
