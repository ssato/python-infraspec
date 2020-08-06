#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import infraspec.files.mount as TT


def test_is_mounted():
    assert TT.is_mounted("/")

# vim:sw=4:ts=4:et:
