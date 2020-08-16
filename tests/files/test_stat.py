#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import infraspec.files.stat as TT


# sha256sum for an empty text file
CSUM = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_has_checksum(tmp_path):
    path = tmp_path / "test.txt"
    path.touch()

    assert not TT.has_checksum(__file__, CSUM)
    assert TT.has_checksum(path, CSUM)
    assert TT.has_checksum(path, CSUM, TT.Checksum.SHA256)


def test_has_size(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("hello, world\n")
    esize = 13

    assert not TT.has_size(__file__, 0)
    assert TT.has_size(path, esize)

# vim:sw=4:ts=4:et:
