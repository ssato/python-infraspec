#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""sysctl tests.
"""
import infraspec.system.sysctl as TT


def test_list():
    assert TT.list()


def test_get():
    assert TT.get("abi.vsyscall32")


def test_is_set():
    assert TT.is_set("abi.vsyscall32", "1")

# vim:sw=4:ts=4:et:
