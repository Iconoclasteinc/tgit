import uuid

from dateutil import parser
from hamcrest import has_properties, is_
from hamcrest.core.base_matcher import BaseMatcher

user_with = has_properties
preferences_with = has_properties
image_with = has_properties
track_with = has_properties
snapshot_with = has_properties
project_with = has_properties


def is_uuid():
    return is_(IsUuidMatcher())


class IsUuidMatcher(BaseMatcher):
    def _matches(self, item):
        try:
            uuid.UUID(item)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

    def describe_to(self, description):
        description.append_text("a UUID compatible string")


def is_date():
    return is_(IsDateMatcher())


class IsDateMatcher(BaseMatcher):
    # noinspection PyBroadException
    def _matches(self, item):
        try:
            parser.parse(item)
            return True
        except Exception:
            return False

    def describe_to(self, description):
        description.append_text("a UTC date compatible string")