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
from datetime import timezone

from dateutil import parser as dateparser


def in_kbps(bps):
    return bps and int(round(bps, -3) / 1000) or ""


def to_duration(seconds):
    return seconds and "%02d:%02d" % divmod(round(seconds), 60) or ""


def as_local_date_time(instant):
    local_time = dateparser.parse(instant).replace(tzinfo=timezone.utc).astimezone()
    return local_time.strftime("%Y-%m-%d"), local_time.strftime("%H:%M:%S")
