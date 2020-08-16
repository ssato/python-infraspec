#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import infraspec.files.permission as TT


def test_has_mode(tmp_path):
    path = tmp_path / "test.txt"
    path.touch()

    mode = 0o750
    path.chmod(mode)

    assert TT.has_mode(path, "750")
    assert not TT.has_mode(path, "644")


def test_is_readable():
    assert TT.is_readable(__file__)
    assert TT.is_readable(__file__, access_by="root")


def test_is_writable():
    assert TT.is_readable(__file__)
    assert TT.is_readable(__file__, access_by="root")


def test_is_executable(tmp_path):
    path = tmp_path / "test.txt"
    path.touch()

    mode = 0o755
    path.chmod(mode)

    assert TT.is_executable(path)
    assert not TT.is_executable(__file__)


def test_is_immutable():
    pass  # TODO

# vim:sw=4:ts=4:et:
