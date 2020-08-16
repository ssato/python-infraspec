#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""User and group tests.
"""
import os
import pwd

import infraspec.common.user_group as TT


try:
    USERNAME = os.getlogin()
except OSError:
    USERNAME = pwd.getpwuid(os.getuid()).pw_name


def test_get_all_groups_itr():
    assert list(TT.get_all_groups_itr())


def test_get_all_groups():
    res = TT.get_all_groups()

    assert res
    assert [usr for usr in res if usr.get("gid") == os.getgid()]

    TT.get_all_groups.cache_clear()


def test_get_user_by_name():
    assert TT.get_user_by_name(USERNAME)
    TT.get_user_by_name.cache_clear()


def test_get_user_by_name_with_group():
    res = TT.get_user_by_name(USERNAME, group=True)

    assert res
    assert res["groups"]

    TT.get_user_by_name.cache_clear()


def test_get_group_by_name():
    usr = TT.get_user_by_name(USERNAME, group=True)
    assert usr["groups"]

    for group in usr["groups"]:
        assert TT.get_group_by_name(group)

    TT.get_user_by_name.cache_clear()
    TT.get_group_by_name.cache_clear()

# vim:sw=4:ts=4:et:
