# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains_string

from test.integration.ui import show_
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message():
    message = messages.close_project_confirmation()
    show_(message)
    return message


def test_shows_confirmation_message(driver):
    _ = show_message()

    driver.shows_message(contains_string("You are about to close the current project."))
    driver.click_yes()
