# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from tgit.announcer import Announcer


class FileChoiceListener(object):
    def fileChosen(self, filename):
        pass


class FileChooser(object):
    def __init__(self):
        super(FileChooser, self).__init__()
        self._listeners = Announcer()

    def chooseFile(self):
        pass

    def addChoiceListener(self, listener):
        self._listeners.addListener(listener)

    def _signalFileChosen(self, filename):
        self._listeners.fileChosen(filename)
