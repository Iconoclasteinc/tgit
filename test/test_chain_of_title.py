import pytest
from hamcrest import assert_that, has_entry, has_entries, not_, has_key, any_of, empty, all_of
from hamcrest import contains, has_property

from test.test_signal import Subscriber
from testing.builders import make_chain_of_title, make_track
from tgit.chain_of_title import ChainOfTitle

pytestmark = pytest.mark.unit


def test_creates_chain_of_title_from_track():
    track = make_track(lyricist=["Joel Miller"], composer=["John Roney"], publisher=["Effendi Records"])
    chain = ChainOfTitle.from_track(track)

    assert_that(chain.contributors,
                all_of(has_author_composer("John Roney", has_entry("name", "John Roney")),
                       has_author_composer("Joel Miller", has_entry("name", "Joel Miller")),
                       has_publisher("Effendi Records", has_entry("name", "Effendi Records"))),
                "The chain of title")


def test_removes_contributor_from_chain_of_title():
    chain_of_title = make_chain_of_title(
        authors_composers=[joel_miller(), john_roney(), contributor("Yoko Ono"), contributor("John Lennon")],
        publishers=[effendi_records(), contributor("Effendi Records")])

    chain_of_title.update(lyricists=["Joel Miller"], composers=["John Lennon"], publishers=["Effendi Records"])

    assert_that(chain_of_title, not_(any_of(has_key("John Roney"), has_key("Yoko Ono"), has_key("Universals"))),
                "The chain of title")


def test_adds_contributor_to_chain_of_title():
    chain_of_title = make_chain_of_title(authors_composers=[joel_miller(), john_roney()],
                                         publishers=[effendi_records()])
    chain_of_title.update(lyricists=["Joel Miller", "John Roney"],
                          composers=["John Roney", "Yoko Ono"],
                          publishers=["Effendi Records", "Universals"])

    assert_that(chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("name", "John Roney")),
                       has_author_composer("Yoko Ono", has_entry("name", "Yoko Ono")),
                       has_publisher("Universals", has_entry("name", "Universals"))),
                "The chain of title")


def test_removes_linked_publisher_from_a_contributor_when_removing_a_publisher():
    chain_of_title = make_chain_of_title(authors_composers=[joel_miller(), john_roney()],
                                         publishers=[effendi_records()])

    chain_of_title.update(lyricists=["Joel Miller"], composers=["John Roney"], publishers=[])

    assert_that(chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("publisher", "")),
                       has_author_composer("Joel Miller", has_entry("publisher", "")),
                       has_entry("publishers", not_(has_key("Effendi Records")))),
                "The chain of title")


def test_signals_chain_of_value_changed_on_contributor_added():
    chain_of_title = make_chain_of_title(authors_composers=[joel_miller(), john_roney()],
                                         publishers=[effendi_records()])

    subscriber = Subscriber()
    chain_of_title.changed.subscribe(subscriber)

    chain_of_title.update(lyricists=["Joel Miller", "Rebecca Ann Maloy"], composers=["John Roney"],
                          publishers=["Effendi Records"])

    assert_that(subscriber.events, contains(contains(has_property("contributors", all_of(
        has_author_composer("John Roney", has_entry("name", "John Roney")),
        has_author_composer("Joel Miller", has_entry("name", "Joel Miller")))))), "The chain of title")


def test_does_not_signal_chain_of_value_when_contributors_have_not_changed():
    chain_of_title = make_chain_of_title(authors_composers=[joel_miller()])

    subscriber = Subscriber()
    chain_of_title.changed.subscribe(subscriber)

    chain_of_title.update(lyricists=["Joel Miller"], composers=[], publishers=[])

    assert_that(subscriber.events, empty(), "The chain of title")


def test_signals_chain_of_value_changed_when_contributor_role_changes_from_lyricist_to_publisher():
    chain_of_title = make_chain_of_title(authors_composers=[joel_miller()])

    subscriber = Subscriber()
    chain_of_title.changed.subscribe(subscriber)

    chain_of_title.update(lyricists=[], publishers=["Joel Miller"], composers=[])

    assert_that(subscriber.events, contains(contains(
        has_property("contributors",
                     has_publisher("Joel Miller", has_entry("name", "Joel Miller"))))), "The chain of title")


def test_updates_contributors():
    chain_of_title = make_chain_of_title(authors_composers=[contributor("Joel Miller"), contributor("John Roney")],
                                         publishers=[contributor("Effendi Records")])

    chain_of_title.update_contributor(**joel_miller())
    chain_of_title.update_contributor(**john_roney())
    chain_of_title.update_contributor(**effendi_records())

    assert_that(chain_of_title.contributors, has_author_composer("Joel Miller", has_entries(joel_miller())),
                "The contributors")
    assert_that(chain_of_title.contributors, has_author_composer("John Roney", has_entries(john_roney())),
                "The contributors")
    assert_that(chain_of_title.contributors, has_publisher("Effendi Records", has_entries(effendi_records())),
                "The contributors")


def has_author_composer(name, matching):
    return has_entry("authors_composers", has_entry(name, matching))


def has_publisher(name, matching):
    return has_entry("publishers", has_entry(name, matching))


def joel_miller():
    return dict(name="Joel Miller", affiliation="SOCAN", publisher="Effendi Records", share="25")


def john_roney():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def yoko_ono():
    return dict(name="Yoko Ono")


def john_lennon():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def effendi_records():
    return dict(name="Effendi Records", share="50")


def contributor(name):
    return dict(name=name)
