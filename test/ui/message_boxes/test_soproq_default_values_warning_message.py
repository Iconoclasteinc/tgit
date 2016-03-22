# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains_string

from test.ui import show_
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message():
    message = messages.default_values_used_for_soproq_export()
    show_(message)
    return message


def test_shows_warning_message(driver):
    _ = show_message()

    driver.shows_message(contains_string("SOPROQ declaration file was generated with default values."))
    driver.click_ok()
