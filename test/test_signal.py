# -*- coding: utf-8 -*-

from hamcrest import assert_that, contains, empty, is_
import pytest

from tgit.signal import Signal, MultiSubscription, Subscription


class Subscriber:
    def __init__(self):
        self.events = []

    def __call__(self, *event):
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


@pytest.fixture()
def multi_value_signal():
    return Signal("multi value signal", int, str)


def event(*value):
    return value


def test_emits_event_to_all_subscribed_listeners(signal):
    subscribers = register_subscribers_to(signal)
    signal.emit('value')
    assert_subscribers_have_been_notified(subscribers, event('value'))


def test_stops_emitting_to_unsubscribed_listeners(signal):
    ex_subscriber = Subscriber()
    signal.subscribe(ex_subscriber)

    subscribers = register_subscribers_to(signal)
    signal.unsubscribe(ex_subscriber)
    assert_that(signal.is_subscribed(ex_subscriber), is_(False), 'subscription still active')

    signal.emit('value')

    assert_that(ex_subscriber.events, empty(), 'events received by ex-subscriber')
    assert_subscribers_have_been_notified(subscribers, event('value'))


def test_registers_same_subscriber_only_once(signal):
    subscriber = Subscriber()
    signal.subscribe(subscriber)
    signal.subscribe(subscriber)

    signal.emit('value')

    assert_that(subscriber.events, contains(event('value')), 'events received only once')


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
    signal.unsubscribe_all()

    signal.emit('event')

    for index, subscriber in enumerate(subscribers):
        assert_that(subscriber.events, empty(), 'events received by subscriber #{}'.format(index))


def test_cancelling_a_multi_subscription_cancels_all_subscriptions(signal):
    subscribers = (Subscriber(), Subscriber(), Subscriber())

    subscriptions = MultiSubscription()

    for subscriber in subscribers:
        subscriptions += signal.subscribe(subscriber)

    subscriptions.cancel()

    for index, subscriber in enumerate(subscribers):
        assert_that(not signal.is_subscribed(subscriber), "subscription #{} still active".format(index))


def test_cancels_subscription_removed_from_a_multi_subscription(signal):
    subscriber = Subscriber()
    subscriptions = MultiSubscription()
    subscription = signal.subscribe(subscriber)
    subscriptions += subscription
    assert_that(signal.is_subscribed(subscriber), "subscription not active")

    subscriptions -= subscription
    assert_that(subscriptions, empty())
    assert_that(not signal.is_subscribed(subscriber), "subscription still active")


def test_signals_can_emit_multiple_values_of_different_types(multi_value_signal):
    subscribers = register_subscribers_to(multi_value_signal)
    multi_value_signal.emit(42, 'text')
    assert_subscribers_have_been_notified(subscribers, event(42, 'text'))
