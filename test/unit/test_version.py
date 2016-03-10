from hamcrest import is_, assert_that
import pytest

from tgit.version import Version

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("lower, higher", [("0.0.0", "0.0.1"),
                                           ("0.0.1", "0.1.0"),
                                           ("0.1.0", "0.1.1"),
                                           ("0.1.1", "1.0.0"),
                                           ("1.0.0", "1.0.1"),
                                           ("1.0.1", "1.1.0"),
                                           ("1.1.0", "1.1.1"),
                                           ("1.1.1", "2.0.0"),
                                           ("1.2.0", "1.10.0")])
def test_is_lower(lower, higher):
    assert_that(Version(lower) < Version(higher), is_(True), lower + " < " + higher)
    assert_that(Version(lower) < higher, is_(True), lower + " < " + higher)


@pytest.mark.parametrize("lower, higher", [("0.0.0", "0.0.0"), ("0.0.0", "0.0.1"),
                                           ("0.0.1", "0.0.1"), ("0.0.1", "0.1.0"),
                                           ("0.1.0", "0.1.0"), ("0.1.0", "0.1.1"),
                                           ("0.1.1", "0.1.1"), ("0.1.1", "1.0.0"),
                                           ("1.0.0", "1.0.0"), ("1.0.0", "1.0.1"),
                                           ("1.0.1", "1.0.1"), ("1.0.1", "1.1.0"),
                                           ("1.1.0", "1.1.0"), ("1.1.0", "1.1.1"),
                                           ("1.1.1", "1.1.1"), ("1.1.1", "2.0.0")])
def test_is_lower_or_equal(lower, higher):
    assert_that(Version(lower) <= Version(higher), is_(True), lower + " <= " + higher)
    assert_that(Version(lower) <= higher, is_(True), lower + " <= " + higher)


@pytest.mark.parametrize("lower, higher", [("0.0.0", "0.0.1"),
                                           ("0.0.1", "0.1.0"),
                                           ("0.1.0", "0.1.1"),
                                           ("0.1.1", "1.0.0"),
                                           ("1.0.0", "1.0.1"),
                                           ("1.0.1", "1.1.0"),
                                           ("1.1.0", "1.1.1"),
                                           ("1.1.1", "2.0.0"),
                                           ("1.2.0", "1.10.0")])
def test_is_higher(lower, higher):
    assert_that(Version(higher) > Version(lower), is_(True), higher + " > " + lower)
    assert_that(Version(higher) > lower, is_(True), higher + " > " + lower)


@pytest.mark.parametrize("lower, higher", [("0.0.0", "0.0.0"), ("0.0.0", "0.0.1"),
                                           ("0.0.1", "0.0.1"), ("0.0.1", "0.1.0"),
                                           ("0.1.0", "0.1.0"), ("0.1.0", "0.1.1"),
                                           ("0.1.1", "0.1.1"), ("0.1.1", "1.0.0"),
                                           ("1.0.0", "1.0.0"), ("1.0.0", "1.0.1"),
                                           ("1.0.1", "1.0.1"), ("1.0.1", "1.1.0"),
                                           ("1.1.0", "1.1.0"), ("1.1.0", "1.1.1"),
                                           ("1.1.1", "1.1.1"), ("1.1.1", "2.0.0")])
def test_is_lower_or_equal(lower, higher):
    assert_that(Version(higher) >= Version(lower), is_(True), higher + " >= " + lower)
    assert_that(Version(higher) >= lower, is_(True), higher + " >= " + lower)


@pytest.mark.parametrize("first, second", [("0.0.0", "0.0.0"),
                                           ("0.0.1", "0.0.1"),
                                           ("0.1.0", "0.1.0"),
                                           ("0.1.1", "0.1.1"),
                                           ("1.0.0", "1.0.0"),
                                           ("1.0.1", "1.0.1"),
                                           ("1.1.0", "1.1.0"),
                                           ("1.1.1", "1.1.1")])
def test_are_equal(first, second):
    assert_that(Version(first) == Version(second), is_(True), first + " == " + second)
    assert_that(Version(first) == second, is_(True), first + " == " + second)


@pytest.mark.parametrize("first, second", [("0.0.0", "0.0.1"),
                                           ("0.1.0", "0.1.1"),
                                           ("1.0.1", "1.0.0"),
                                           ("1.1.1", "1.1.0")])
def test_are_not_equal(first, second):
    assert_that(Version(first) != Version(second), is_(True), first + " != " + second)
    assert_that(Version(first) != second, is_(True), first + " != " + second)
