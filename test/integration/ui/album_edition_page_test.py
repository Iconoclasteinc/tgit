# -*- coding: utf-8 -*-

import timeit

from hamcrest import has_entries, assert_that, less_than

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import AlbumEditionPageDriver
from test.integration.ui import WidgetTest
from test.util import resources, builders as build
from tgit.metadata import Image
from tgit.preferences import Preferences
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.util import fs


class AlbumEditionPageTest(WidgetTest):
    def render(self, album):
        self.page = AlbumEditionPage(Preferences(), use_local_isni_backend=True)
        self.page.refresh(album)
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)

    def createDriverFor(self, widget):
        return AlbumEditionPageDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testDisplaysPicturePlaceholderWhenAlbumHasNoCover(self):
        self.render(build.album())
        self.driver.showsPicturePlaceholder()

    def testDisplaysMainAlbumCoverWhenExisting(self):
        self.render(
            build.album(images=[build.image("image/jpeg", loadTestImage("front-cover.jpg"), Image.FRONT_COVER)]))
        self.driver.showsPicture()

    def testDisplaysAlbumMetadata(self):
        self.render(build.album(
            release_name="Album",
            lead_performer="Artist",
            isni="123456789",
            guest_performers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
            label_name="Label",
            catalog_number="XXX123456789",
            upc="123456789999",
            recording_time="2008-09-15",
            release_time="2009-01-01",
            recording_studios="Studio A, Studio B",
            producer="Artistic Producer",
            mixer="Mixing Engineer",
            comments="Comments\n...",
            primary_style="Style"))

        self.driver.showsReleaseName("Album")
        self.driver.shows_compilation(False)
        self.driver.shows_lead_performer("Artist")
        self.driver.shows_isni("123456789", True)
        self.driver.showsArea("")
        self.driver.showsGuestPerformers("Guitar: Guitarist; Piano: Pianist")
        self.driver.showsLabelName("Label")
        self.driver.showsCatalogNumber("XXX123456789")
        self.driver.showsUpc("123456789999")
        self.driver.shows_recording_time("2008-09-15")
        self.driver.showsReleaseTime("2009-01-01")
        self.driver.showsDigitalReleaseTime("2000-01-01")
        self.driver.showsRecordingStudios("Studio A, Studio B")
        self.driver.showsProducer("Artistic Producer")
        self.driver.showsMixer("Mixing Engineer")
        self.driver.showsComments("Comments\n...")
        self.driver.shows_primary_style("Style")
        self.driver.showsMediaType("")
        # self.driver.showsReleaseType("")

    def testIndicatesWhetherAlbumIsACompilation(self):
        album = build.album(compilation=False)
        self.render(album)
        self.driver.shows_compilation(False)

        album.compilation = True
        self.page.refresh(album)
        self.driver.shows_compilation(True)

    def testDisablesLeadPerformerEditionWhenAlbumIsACompilation(self):
        self.render(build.album(compilation=True, lead_performer="Album Artist"))
        self.driver.shows_lead_performer("Various Artists", disabled=True)

    def testTogglesLookupISNIButtonWhenAlbumIsNoLongerACompilation(self):
        album = build.album(compilation=True, lead_performer="Album Artist")
        self.render(album)
        self.driver.enablesISNILookup(False)

        album.compilation = False
        self.page.refresh(album)
        self.driver.enablesISNILookup()

    def testDisablesLookupISNIButtonWhenAlbumIsACompilation(self):
        self.render(build.album(compilation=True, lead_performer="Album Artist"))
        self.driver.enablesISNILookup(False)

    def testDisablesLookupISNIButtonWhenLeadPerformerIsEmpty(self):
        self.render(build.album(lead_performer=""))
        self.driver.enablesISNILookup(False)

    def testDisablesLookupISNIButtonWhenLeadPerformerIsBlank(self):
        self.render(build.album(lead_performer="     "))
        self.driver.enablesISNILookup(False)

    def test_enables_assign_isni_button_when_lead_performer_is_not_empty(self):
        self.render(build.album(lead_performer="performer"))
        self.driver.enablesISNIAssign()

    def testDisablesAssignISNIButtonWhenLeadPerformerIsNotEmpty(self):
        self.render(build.album())
        self.driver.enablesISNIAssign(False)

    def testSignalsWhenPictureSelected(self):
        self.render(build.album())

        select_picture_signal = ValueMatcherProbe("select picture")
        self.page.select_picture.connect(select_picture_signal.received)

        self.driver.addPicture()
        self.check(select_picture_signal)

    def testSignalsWhenAddingAPerformer(self):
        self.render(build.album())

        addPerformerSignal = ValueMatcherProbe("add performer")
        self.page.add_performer.connect(addPerformerSignal.received)

        self.driver.addPerformer()
        self.check(addPerformerSignal)

    def testEfficientlyDisplaysImageCoverWhenItDoesNotChange(self):
        album = build.album(images=[build.image("image/jpeg", loadTestImage("big-image.jpg"), Image.FRONT_COVER)])
        self.render(album)

        time = timeit.timeit(lambda: self.page.refresh(album), number=50)
        assert_that(time, less_than(1), "time to execute render 50 times")

    def testSignalsWhenRemovePictureButtonClicked(self):
        self.render(build.album())

        removePictureSignal = ValueMatcherProbe("remove picture")
        self.page.remove_picture.connect(removePictureSignal.received)

        self.driver.removePicture()
        self.check(removePictureSignal)

    def test_signals_when_lookup_isni_button_clicked(self):
        self.render(build.album(lead_performer="performer"))

        lookup_isni_signal = ValueMatcherProbe("lookup ISNI")
        self.page.lookup_isni.connect(lookup_isni_signal.received)

        self.driver.lookup_isni_of_lead_performer()
        self.check(lookup_isni_signal)

    def test_signals_when_clear_isni_button_clicked(self):
        self.render(build.album(isni="0000123456789"))

        clear_isni_signal = ValueMatcherProbe("clear ISNI")
        self.page.clear_isni.connect(clear_isni_signal.received)

        self.driver.clear_isni()
        self.check(clear_isni_signal)

    def test_signals_when_assign_isni_button_clicked(self):
        self.render(build.album(lead_performer="performer"))

        assign_isni_signal = ValueMatcherProbe("assign ISNI")
        self.page.assign_isni.connect(assign_isni_signal.received)

        self.driver.assign_isni_to_lead_performer()
        self.check(assign_isni_signal)

    def testSignalsWhenAlbumMetadataEdited(self):
        self.render(build.album())

        metadata_changed_signal = ValueMatcherProbe("metadata changed")
        self.page.metadata_changed.connect(metadata_changed_signal.received)

        metadata_changed_signal.expect(has_entries(release_name="Title"))
        self.driver.changeReleaseName("Title")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(compilation=True))
        self.driver.toggle_compilation()
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(compilation=False))
        self.driver.toggle_compilation()
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(lead_performer="Artist"))
        self.driver.changeLeadPerformer("Artist")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(
            guest_performers=[("Guitar", "Guitarist"), ("Guitar", "Bassist"), ("Piano", "Pianist")]))
        self.driver.changeGuestPerformers("Guitar: Guitarist; Guitar: Bassist; Piano: Pianist")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(label_name="Label"))
        self.driver.changeLabelName("Label")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(catalog_number="XXX12345678"))
        self.driver.changeCatalogNumber("XXX12345678")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(upc="123456789999"))
        self.driver.changeUpc("123456789999")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(comments="Comments\n...\n"))
        self.driver.addComments("Comments")
        self.driver.addComments("...")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(release_time="2009-01-01"))
        self.driver.changeReleaseTime(2009, 1, 1)
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(recording_time="2008-09-15"))
        self.driver.change_recording_time(2008, 9, 15)
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(recording_studios="Studios"))
        self.driver.changeRecordingStudios("Studios")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(producer="Producer"))
        self.driver.changeProducer("Producer")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(mixer="Mixer"))
        self.driver.changeMixer("Mixer")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(primary_style="Jazz"))
        self.driver.select_primary_style("Jazz")
        self.check(metadata_changed_signal)

        metadata_changed_signal.expect(has_entries(primary_style="Custom"))
        self.driver.changePrimaryStyle("Custom")
        self.check(metadata_changed_signal)


def loadTestImage(name):
    return fs.read(resources.path(name))