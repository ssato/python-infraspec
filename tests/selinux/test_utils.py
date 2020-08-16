#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import pytest

import infraspec.selinux.utils as TT


try:
    TT.get_selinux_label(__file__)
    SELINUX_WORKS = True
except OSError:
    SELINUX_WORKS = False


@pytest.mark.skipif(not SELINUX_WORKS,
                    reason="SELinux does not work as expected.")
def test_has_selinux_label():
    slabel = "unconfined_u:object_r:user_home_t:s0"
    assert TT.has_selinux_label(__file__, slabel, strict=True)
    assert TT.has_selinux_label(__file__, slabel[:-3])
    assert not TT.has_selinux_label(__file__, slabel[:-3], strict=True)

# vim:sw=4:ts=4:et:
