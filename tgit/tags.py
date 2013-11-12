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

# todo move tags to album.py

FRONT_COVER = 'frontCover'

RELEASE_NAME = 'releaseName'
LEAD_PERFORMER = 'leadPerformer'
GUEST_PERFORMERS = 'guestPerformers'
LABEL_NAME = 'labelName'
UPC = 'upc'
CATALOG_NUMBER = 'catalogNumber'
RELEASE_TIME = 'releaseTime'
ORIGINAL_RELEASE_TIME = 'originalReleaseTime'
RECORDING_TIME = 'recordingTime'
RECORDING_STUDIOS = 'recordingStudios'
PRODUCER = 'producer'
MIXER = 'mixer'
CONTRIBUTORS = 'contributors'
COMMENTS = 'comments'


ALBUM_TAGS = [
    RELEASE_NAME,
    LEAD_PERFORMER,
    GUEST_PERFORMERS,
    LABEL_NAME,
    UPC,
    CATALOG_NUMBER,
    RECORDING_TIME,
    RELEASE_TIME,
    ORIGINAL_RELEASE_TIME,
    RECORDING_STUDIOS,
    PRODUCER,
    MIXER,
    CONTRIBUTORS,
    COMMENTS
]

# todo move tags to track.py

BITRATE = 'bitrate'
DURATION = 'duration'
TRACK_TITLE = 'trackTitle'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
LYRICIST = 'lyricist'
COMPOSER = 'composer'
PUBLISHER = 'publisher'
ISRC = 'isrc'
TAGS = 'tags'
LYRICS = 'lyrics'

TRACK_TAGS = [
    TRACK_TITLE,
    VERSION_INFO,
    FEATURED_GUEST,
    PUBLISHER,
    LYRICIST,
    COMPOSER,
    ISRC,
    TAGS,
    LYRICS,
    BITRATE,
    DURATION,
]




