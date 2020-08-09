#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""SELinux tests.
"""
import pathlib

import infraspec.selinux.selinux_ as TT


# from /etc/selinux/config
_CNF_CONTENT_1 = """

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected ...
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

"""

_CNF_1 = dict(SELINUX="enforcing", SELINUXTYPE="targeted")


def test_is_selinux_enabled():
    assert not TT.is_selinux_enabled(pathlib.Path(__file__).parent)
    TT.is_selinux_enabled.cache_clear()

    assert TT.is_selinux_enabled("/")  # see its impl.
    TT.is_selinux_enabled.cache_clear()


def test_get_config(tmpdir):
    root = "/"
    path = pathlib.Path(tmpdir) / "config"

    assert TT.get_config(path, root) == {}
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()

    path.write_text(_CNF_CONTENT_1)
    assert TT.get_config(path, root) == _CNF_1
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()


def test_get_mode(tmpdir):
    root = "/"
    path = pathlib.Path(tmpdir) / "config"

    assert TT.get_mode(path, root) == "disabled"
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()

    path.write_text(_CNF_CONTENT_1)
    assert TT.get_mode(path, root) == "enforcing"
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()


def test_get_policy_type(tmpdir):
    root = "/"
    path = pathlib.Path(tmpdir) / "config"

    assert TT.get_policy_type(path, root) == "targeted"
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()

    path.write_text(_CNF_CONTENT_1)
    assert TT.get_policy_type(path, root) == "targeted"
    TT.is_selinux_enabled.cache_clear()
    TT.get_config.cache_clear()

# vim:sw=4:ts=4:et:
