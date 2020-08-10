#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""SELinux tests.
"""
import pathlib

import pytest

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


def get_root_and_path(tmpdir, write_config=False):
    TT.is_enabled.cache_clear()
    TT.get_config.cache_clear()
    (root, path) = ("/", pathlib.Path(tmpdir) / "config")

    if write_config:
        path.write_text(_CNF_CONTENT_1)

    return (root, path)


def test_is_enabled():
    assert not TT.is_enabled(pathlib.Path(__file__).parent)
    TT.is_enabled.cache_clear()

    assert TT.is_enabled("/")  # see its impl.
    TT.is_enabled.cache_clear()


def test_get_config__default(tmpdir):
    (root, path) = get_root_and_path(tmpdir)

    assert TT.get_config(path, root) == {}


def test_get_config__from_file(tmpdir):
    (root, path) = get_root_and_path(tmpdir, True)

    assert TT.get_config(path, root) == _CNF_1


def test_get_mode__empty_config(tmpdir):
    (root, path) = get_root_and_path(tmpdir)

    assert TT.get_mode(path, root) == "disabled"


def test_get_mode__from_file(tmpdir):
    (root, path) = get_root_and_path(tmpdir, True)

    assert TT.get_mode(path, root) == "enforcing"


def test_get_policy_type__default(tmpdir):
    (root, path) = get_root_and_path(tmpdir)

    assert TT.get_policy_type(path, root) == "targeted"


def test_get_policy_type__from_file(tmpdir):
    (root, path) = get_root_and_path(tmpdir, True)

    assert TT.get_policy_type(path, root) == "targeted"


def test_is_enforcing__disabled(tmpdir):
    (root, path) = get_root_and_path(tmpdir)
    assert not TT.is_enforcing(path, root)


def test_is_enforcing__enabled(tmpdir):
    (root, path) = get_root_and_path(tmpdir, True)

    assert TT.is_enforcing(path, root)


def test_is_enforcing__with_policy(tmpdir):
    (root, path) = get_root_and_path(tmpdir, True)

    assert not TT.is_enforcing(path, root, "mls")
    assert TT.is_enforcing(path, root, "targeted")


def test_is_permissive(tmpdir):
    (root, path) = get_root_and_path(tmpdir)
    assert not TT.is_permissive(path, root)


def test_is_disabled(tmpdir):
    (root, path) = get_root_and_path(tmpdir)
    assert not TT.is_disabled(path, root)

# vim:sw=4:ts=4:et:
