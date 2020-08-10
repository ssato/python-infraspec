#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import pytest

try:
    import infraspec.selinux.utils as TT
except AttributeError:
    TT = False


@pytest.mark.skipif(not TT, reason="Necessary module is not available")
def test_has_selinux_label():
    slabel = "unconfined_u:object_r:user_home_t:s0"  # TODO
    assert TT.has_selinux_label(__file__, slabel, strict=True)
    assert TT.has_selinux_label(__file__, slabel[:-3])
    assert not TT.has_selinux_label(__file__, slabel[:-3], strict=True)

# vim:sw=4:ts=4:et: