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

def inKbps(bps):
    return int(round(bps, -3) / 1000)


def asDuration(seconds):
    return '%02d:%02d' % divmod(round(seconds), 60)


def toPeopleList(people):
    return '; '.join(['%s: %s' % (role, name) for role, name in people])


def fromPeopleList(text):
    people = []
    involvements = text.split(';')

    for involvement in involvements:
        try:
            role, name = involvement.split(':')
            people.append((role.strip(), name.strip()))
        except ValueError:
            pass

    return people