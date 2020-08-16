#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""Group (linux) tests.
"""
import infraspec.group.linux as TT


def test_get():
    assert TT.get("root")
    assert TT.get("group_should_not_exist") is None


def test_get_gid():
    assert TT.get_gid("root") == 0
    assert TT.get_gid("group_should_not_exist") is None


def test_exist():
    assert TT.exist("root")
    assert not TT.exist("group_should_not_exist")


def test_have_gid():
    assert TT.have_gid("root", 0)
    assert not TT.have_gid("root", 1000)
    assert not TT.have_gid("group_should_not_exist", 0)

# vim:sw=4:ts=4:et:
