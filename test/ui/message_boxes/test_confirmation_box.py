# -*- coding: utf-8 -*-
import pytest

from cute.probes import ValueMatcherProbe
from test.ui import show_, ignore
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message(on_accept=ignore):
    message = messages.overwrite_project_confirmation(on_accept=on_accept)
    show_(message)
    return message


def test_signals_when_confirmed(driver):
    accept_signal = ValueMatcherProbe("accept confirmation")
    _ = show_message(on_accept=accept_signal.received)

    driver.click_yes()
    driver.check(accept_signal)
