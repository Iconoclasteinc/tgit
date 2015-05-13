# -*- coding: utf-8 -*-

from hamcrest import assert_that, contains, empty, is_
import pytest
from tgit.signal import Signal


class Subscriber(object):
    def __init__(self):
        self.events = []

    def __call__(self, event):
        self.events.append(event)


SUBSCRIBERS_COUNT = 5


def register_subscribers_to(signal_):
    subscribers = []
    for i in range(SUBSCRIBERS_COUNT):
        subscribers.append(register_new_subscriber(signal_))

    return subscribers


def register_new_subscriber(signal_):
    subscriber = Subscriber()
    signal_.subscribe(subscriber)
    assert_that(signal_.is_subscribed(subscriber), is_(True), 'subscription active')
    return subscriber


def assert_subscribers_have_been_notified(subscribers, *events):
    for number, subscriber in enumerate(subscribers):
        assert_that(subscriber.events, contains(*events), 'subscriber #{} events'.format(number + 1))


@pytest.fixture
def signal():
    return Signal("signal", str)


def test_signals_event_to_all_subscribed_listeners(signal):
    subscribers = register_subscribers_to(signal)
    signal.emit('event')
    assert_subscribers_have_been_notified(subscribers, 'event')


def test_stops_emitting_to_unsubscribed_listeners(signal):
    ex_subscriber = Subscriber()
    signal.subscribe(ex_subscriber)

    subscribers = register_subscribers_to(signal)
    signal.unsubscribe(ex_subscriber)
    assert_that(signal.is_subscribed(ex_subscriber), is_(False), 'subscription still active')

    signal.emit('event')

    assert_that(ex_subscriber.events, empty(), 'events received by ex-subscriber')
    assert_subscribers_have_been_notified(subscribers, 'event')


def test_registers_same_subscriber_only_once(signal):
    subscriber = Subscriber()
    signal.subscribe(subscriber)
    signal.subscribe(subscriber)

    signal.emit('event')

    assert_that(subscriber.events, contains('event'), 'events received only once')


def test_cancelling_a_subscription_unregisters_the_subscriber(signal):
    subscriber = Subscriber()
    subscription = signal.subscribe(subscriber)
    subscription.cancel()

    assert_that(signal.is_subscribed(subscriber), is_(False), 'subscription still active')


def test_will_not_emit_events_of_incompatible_type(signal):
    with pytest.raises(TypeError):
        signal.emit(1)


def test_can_unsubscribe_all_listeners_at_once(signal):
    subscribers = register_subscribers_to(signal)
    signal.unsubscribe()

    signal.emit('event')

    for index, subscriber in enumerate(subscribers):
        assert_that(subscriber.events, empty(), 'events received by subscriber #{}'.format(index))