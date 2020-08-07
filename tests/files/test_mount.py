#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import sys

import pytest

import infraspec.files.mount as TT


@pytest.mark.skipif(sys.version_info < (3, 7),
                    reason="skipping becuase pathlib.Path.is_mount is "
                           "not available.")
def test_is_mounted():
    assert TT.is_mounted("/")
    assert TT.is_mounted("/proc", with_=dict(type="proc"))

# vim:sw=4:ts=4:et:
