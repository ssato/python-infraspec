#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""Package (rpm) tests.
"""
import pytest

import infraspec.package.rpm as TT


RPM_IS_NOT_AVAIL = False
try:
    PKG_FULL = TT.subprocess.run(
        "rpm -q rpm".split(), stdout=TT.subprocess.PIPE
    ).stdout.decode("utf-8").rstrip()

    (PKG_NAME, PKG_VER) = TT.subprocess.run(
        "rpm -q --qf %{n},%{v} rpm".split(), stdout=TT.subprocess.PIPE
    ).stdout.decode("utf-8").rstrip().split(',')

except (AttributeError, ValueError):
    RPM_IS_NOT_AVAIL = True
    PKG_FULL = PKG_NAME = PKG_VER = None


@pytest.mark.skipif(RPM_IS_NOT_AVAIL, reason="Could not get rpm package info.")
@pytest.mark.parametrize("name,ver,expected", (
    ("pkg-not-exist", None, None),
    (PKG_NAME, None, PKG_FULL),
    (PKG_NAME, PKG_VER, PKG_FULL)
))
def test_get_installed(name, ver, expected):
    assert TT.get_installed(name, version=ver) == expected


@pytest.mark.skipif(RPM_IS_NOT_AVAIL, reason="Could not get rpm package info.")
@pytest.mark.parametrize("name,ver,expected", (
    ("pkg-not-exist", None, False),
    (PKG_NAME, None, True),
    (PKG_NAME, PKG_VER, True)
))
def test_is_installed(name, ver, expected):
    assert TT.is_installed(name, version=ver) == expected

# vim:sw=4:ts=4:et:
