from flexmock import flexmock
import pytest

from tgit.announcer import Announcer

pytestmark = pytest.mark.unit


class Listener(object):
    def event_occurred(self, event):
        pass


@pytest.fixture
def announcer():
    return Announcer()


@pytest.fixture
def event():
    return "event"


def test_announces_to_all_subscribed_listeners(announcer, event):
    _listeners_are_subscribed(announcer, event)
    announcer.event_occurred(event)


def test_stops_announcing_to_unregistered_listeners(announcer, event):
    should_not_notified = flexmock(Listener())
    announcer.addListener(should_not_notified)

    _listeners_are_subscribed(announcer, event)
    announcer.removeListener(should_not_notified)

    should_not_notified.should_receive("event_occurred").never()
    announcer.event_occurred(event)


def _listeners_are_subscribed(announcer, event):
    for i in range(5):
        _subscribe_listener(announcer, event)


def _subscribe_listener(announcer, event):
    listener = flexmock(Listener())
    listener.should_receive("event_occurred").with_args(event).once()
    announcer.addListener(listener)
