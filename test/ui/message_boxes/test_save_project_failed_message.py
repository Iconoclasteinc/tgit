# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains_string

from test.ui import show_
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message():
    message = messages.save_project_failed()
    show_(message)
    return message


def test_shows_error_message(driver):
    _ = show_message()

    driver.shows_message(contains_string("Your project file could not be saved."))
    driver.click_ok()
