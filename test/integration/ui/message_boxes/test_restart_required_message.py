# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains_string

from test.integration.ui import show_
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message():
    message = messages.restart_required()
    show_(message)
    return message


def test_shows_information_message(driver):
    _ = show_message()

    driver.shows_message(contains_string("You need to restart TGiT for changes to take effect."))
    driver.click_ok()
