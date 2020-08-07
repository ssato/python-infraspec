#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import pytest

import infraspec.files.selinux_ as TT

try:
    import selinux
    selinux.getfilecon  # noqa: F401
    SELINUX_IS_NOT_AVAIL = False
except AttributeError:
    SELINUX_IS_NOT_AVAIL = True


@pytest.mark.skipif(SELINUX_IS_NOT_AVAIL,
                    reason="selinux.getfilecon is not available")
def test_has_selinux_label():
    slabel = "unconfined_u:object_r:user_home_t:s0"  # TODO
    assert TT.has_selinux_label(__file__, slabel, strict=True)
    assert TT.has_selinux_label(__file__, slabel[:-3])
    assert not TT.has_selinux_label(__file__, slabel[:-3], strict=True)

# vim:sw=4:ts=4:et:
