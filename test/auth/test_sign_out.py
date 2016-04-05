from hamcrest import assert_that, is_

from testing.builders import make_registered_session
from tgit.auth import sign_out_from


def test_signs_user_out():
    session = make_registered_session("...", "...")

    sign_out_from(session)()

    assert_that(session.opened, is_(False), "opened session")
