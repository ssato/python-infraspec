#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""User (linux) tests.
"""
import os
import pwd

import pytest

import infraspec.user.linux as TT


try:
    USERNAME = os.getlogin()
except OSError:
    USERNAME = pwd.getpwuid(os.getuid()).pw_name


def test_get():
    assert TT.get(USERNAME)
    assert TT.get("user_should_not_exist") is None


def test_get_attr():
    for attr in TT.VALID_ATTRS:
        assert TT.get_attr(USERNAME, attr) is not None

    with pytest.raises(ValueError) as exc:
        TT.get_attr(USERNAME, "attr_should_not_exist")

    assert "User attribute must be one of" in str(exc.value)


def test_exist():
    assert TT.exist(USERNAME)
    assert TT.exist("root")
    assert not TT.exist("user_should_not_exist")


def test_belong_to_group():
    assert TT.belong_to_group("root", "root")


def test_belong_to_primary_group():
    assert TT.belong_to_primary_group("root", "root")


def test_have_attr_x():
    assert TT.have_attr_x("name", USERNAME, USERNAME)
    assert TT.have_attr_x("uid", "root", 0)
    assert not TT.have_attr_x("uid", "root", 1000)

# vim:sw=4:ts=4:et:
