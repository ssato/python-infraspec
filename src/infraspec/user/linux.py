#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#user
# ref. https://testinfra.readthedocs.io/en/latest/modules.html#user
#
"""User related tests.
"""
import functools
import typing

from ..common import (
    get_user_by_name, get_group_by_name, get_group_by_gid
)


UserAttrT = typing.Union[int, str]

# .. seealso:: :functio:`infraspec.common.user_group.get_user_by_name`
VALID_ATTRS = frozenset(
    "uid gid name gecos homedir groups shell".split()
)


def get(username: str) -> typing.Optional[typing.Mapping]:
    """
    Get user's info by user name.
    """
    return get_user_by_name(username)


def get_attr(username: str, attr: str,
             valid_attrs: typing.Iterable[str] = VALID_ATTRS
             ) -> typing.Optional[UserAttrT]:
    """
    Get user's info by user name.
    """
    if attr not in valid_attrs:
        raise ValueError("User attribute must be one of [{}] but got "
                         "{}".format(", ".join(valid_attrs), attr))

    user = get(username)

    return None if user is None else user.get(attr, None)


def exist(username: str) -> bool:
    """
    Does the user `username` exist?
    """
    return get(username) is not None


def belong_to_group(username: str, groupname: str) -> bool:
    """
    Does the user `username` belong the group `groupname`?
    """
    user = get(username)

    if user is None:
        return False

    # 1. Try match with primary group.
    group = get_group_by_gid(user["gid"])

    if group and group["name"] == groupname:
        return True

    # 2. Try match with other groups.
    group = get_group_by_name(groupname)

    if group is None:
        return False

    return username in group["members"]


def belong_to_primary_group(username: str, groupname: str) -> bool:
    """
    Does the user `username` belong the primary group `groupname`?
    """
    user = get(username)

    if user is None:
        return False

    group = get_group_by_gid(user["gid"])

    if group is None:  # I think it never happen but just in case.
        return False

    return group["name"] == groupname


def have_attr_x(attr: str, username: str, value: typing.Any,
                valid_attrs: typing.Iterable[str] = VALID_ATTRS) -> bool:
    """
    Does the attribute of the user `username` have given value?
    """
    return get_attr(username, attr, valid_attrs=valid_attrs) == value


# Aliases and other callables.
# pylint: disable=invalid-name
exists = exist
is_in_group = belong_to_group

have_uid = functools.partial(have_attr_x, "uid")
have_home_directory = have_homedir = functools.partial(have_attr_x, "homedir")
have_login_shell = have_shell = functools.partial(have_attr_x, "shell")

# vim:sw=4:ts=4:et:
