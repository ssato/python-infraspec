#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#group
# ref. https://testinfra.readthedocs.io/en/latest/modules.html#group
#
"""User related tests.
"""
import typing

from ..common import get_group_by_name


def get(name: str) -> typing.Optional[typing.Mapping]:
    """
    Get group's info by name.
    """
    return get_group_by_name(name)


def get_gid(name: str) -> typing.Optional[int]:
    """
    Get the gid of the group `name`.
    """
    group = get(name)

    if group is None:
        return None

    return group["gid"]


def exist(name: str) -> bool:
    """
    Does the group `name` exist?
    """
    return get(name) is not None


def have_gid(name: str, gid: int) -> bool:
    """
    Does the gid of the group `name` match with the value `gid`?
    """
    group = get(name)

    if group is None:
        return False

    return group["gid"] == gid


# Aliases and other callables.
# pylint: disable=invalid-name
exists = exist

# vim:sw=4:ts=4:et:
