#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""SELinux modules tests.
"""
import os
import pytest

import infraspec.selinux.modules as TT


@pytest.mark.skipif(os.getuid() != 0, reason="You're not root")
def test_list_modules():
    assert TT.list_modules()


@pytest.mark.skipif(os.getuid() != 0, reason="You're not root")
def test_is_installed():
    assert not TT.is_installed("not_exist_selinux_module")
    assert TT.is_installed("dmesg")

# vim:sw=4:ts=4:et:
