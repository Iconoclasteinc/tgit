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


class signal:
    """Descriptor class for signals"""
    def __init__(self, *types, name=None):
        self.name = name
        self._types = types

    def __get__(self, instance, owner):
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = Signal(self.name, *self._types)
        return instance.__dict__[self.name]


class Subscription:
    """Subscription are returned from `Signal.subscribe` to allow unsubscribing"""
    def __init__(self, observable, subscriber):
        self._observable = observable
        self._subscriber = subscriber

    @property
    def observable(self):
        return self._observable

    def cancel(self):
        self._observable.unsubscribe(self._subscriber)


class MultiSubscription:
    """Groups multiple Subscriptions together and unsubscribes from all of them together"""
    def __init__(self):
        self._subscriptions = []

    def __iadd__(self, subscription):
        self.add(subscription)
        return self

    def __isub__(self, subscription):
        self.remove(subscription)
        return self

    def __iter__(self):
        return iter(self._subscriptions)

    def __len__(self):
        return len(self._subscriptions)

    def add(self, subscription):
        self._subscriptions.append(subscription)

    def remove(self, subscription):
        self._subscriptions.remove(subscription)
        subscription.cancel()

    def cancel(self):
        for subscription in self._subscriptions:
            subscription.cancel()


class Observable(type):
    """Metaclass for Observable types that have signals"""
    def __new__(mcs, clsname, bases, methods):
        # Attach names to the signals
        for key, value in methods.items():
            if isinstance(value, signal) and not value.name:
                value.name = key
        return super().__new__(mcs, clsname, bases, methods)


class Signal:
    """A signal emits events and allows subscribing and unsubscribing"""
    def __init__(self, name, *types):
        self._name = name
        self._types = types
        self._subscribers = []

    @property
    def subscribers(self):
        return list(self._subscribers)

    def emit(self, *event):
        for index, (value, type_) in enumerate(zip(event, self._types)):
            if not isinstance(value, type_):
                raise TypeError("{0} event should have parameter {1} of type {2}, not {3}".format(
                    self._name, index, type_.__name__, type(value).__name__))

        for subscriber in self._subscribers:
            subscriber(*event)

    def subscribe(self, subscriber):
        if not callable(subscriber):
            raise TypeError("Subscriber does not seem callable: " + type(subscriber).__name__)

        if not self.is_subscribed(subscriber):
            self._subscribers.append(subscriber)
            return Subscription(self, subscriber)

    def _remove(self, subscriber):
        if self.is_subscribed(subscriber):
            self._subscribers.remove(subscriber)

    def is_subscribed(self, subscriber):
        return subscriber in self._subscribers

    def unsubscribe(self, *subscribers):
        for subscriber in subscribers:
            self._remove(subscriber)

    def unsubscribe_all(self):
        self.unsubscribe(*self._subscribers)