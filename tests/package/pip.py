#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""Package (pip) tests.
"""
import pytest

import infraspec.package.pip as TT


try:
    TT.subprocess.run(["pip", "--help"], check=True)
    PIP_IS_NOT_AVAIL = False
    REASON = ''

except FileNotFoundError:
    PIP_IS_NOT_AVAIL = True
    REASON = "pip is not available in your system."


@pytest.mark.skipif(PIP_IS_NOT_AVAIL, reason=REASON)
@pytest.mark.parametrize("path,outdated,expected", (
    (None, False, True),
    (None, True, True),
    ("tmp", False, False),
    ("tmp", True, False),
))
def test_list_installed(path, outdated, expected):
    assert bool(TT.list_installed(path=path, outdated=outdated)) == expected


@pytest.mark.skipif(PIP_IS_NOT_AVAIL, reason=REASON)
@pytest.mark.parametrize("name,version,expected", (
    ("pkg-not-exist", None, False),
    ("pip", None, True),
))
def test_get_installed(name, version, expected):
    assert bool(TT.get_installed(name, version=version)) == expected


@pytest.mark.skipif(PIP_IS_NOT_AVAIL, reason=REASON)
@pytest.mark.parametrize("name,version,expected", (
    ("pkg-not-exist", None, False),
    ("pip", None, True),
))
def test_is_installed(name, version, expected):
    assert bool(TT.is_installed(name, version=version)) == expected

# vim:sw=4:ts=4:et:
