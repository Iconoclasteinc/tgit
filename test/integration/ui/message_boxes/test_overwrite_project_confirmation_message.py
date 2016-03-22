# -*- coding: utf-8 -*-
import pytest
from hamcrest import contains_string

from test.integration.ui import show_
from tgit.ui import message_boxes as messages

pytestmark = pytest.mark.ui


def show_message():
    message = messages.overwrite_project_confirmation()
    show_(message)
    return message


def test_shows_overwrite_project_confirmation_message(driver):
    _ = show_message()

    driver.shows_message(contains_string("This project already exists."))
