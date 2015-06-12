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
from tgit.signal import MultiSubscription


def Observer(cls):
    """Decorator for widgets observing event signals"""
    widget_close = cls.close

    @property
    def subscriptions(self):
        if not hasattr(self, '_subscriptions'):
            self._subscriptions = MultiSubscription()

        return self._subscriptions

    def subscribe(self, signal, subscriber):
        self.subscriptions.add(signal.subscribe(subscriber))

    def unsubscribe(self, signal):
        for subscription in self.subscriptions:
            if subscription.observable == signal:
                self.subscriptions.remove(subscription)

    def close(self):
        self.subscriptions.cancel()
        return widget_close(self)

    cls.subscribe = subscribe
    cls.unsubscribe = unsubscribe
    cls.close = close
    cls.subscriptions = subscriptions

    return cls
