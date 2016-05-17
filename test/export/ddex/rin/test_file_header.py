# -*- coding: utf-8 -*-
import os

from hamcrest import assert_that, equal_to
import pytest

from testing.matchers import is_uuid, is_date
from tgit.export.ddex.rin.file_header import FileHeader

pytestmark = pytest.mark.unit


def test_writes_uuid_as_file_id(root, tmpdir):
    FileHeader(os.path.join(tmpdir.strpath, "Honeycomb.xml")).write_to(root)

    assert_that(root.findtext("./FileHeader/FileId"), is_uuid(), "The file id")


def test_writes_file_created_date(root, tmpdir):
    FileHeader(os.path.join(tmpdir.strpath, "Honeycomb.xml")).write_to(root)

    assert_that(root.findtext("./FileHeader/FileCreatedDateTime"), is_date(), "The file creation date")


def test_writes_file_name(root, tmpdir):
    FileHeader(os.path.join(tmpdir.strpath, "Honeycomb.xml")).write_to(root)

    assert_that(root.findtext("./FileHeader/FileName"), equal_to("Honeycomb.xml"), "The file name")
