#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Utility functions to get users info.
"""
import functools
import grp
import operator
import pwd
import typing


def get_all_groups_itr() -> typing.Iterator[typing.Mapping]:
    """
    Get all groups' info from group data base.
    """
    for ginfo in grp.getgrall():
        yield dict(gid=ginfo.gr_gid, name=ginfo.gr_name,
                   members=ginfo.gr_mem)


@functools.lru_cache(maxsize=8)
def get_all_groups() -> typing.List[typing.Mapping]:
    """
    Get all groups' info from group data base.
    """
    return sorted(get_all_groups_itr(), key=operator.itemgetter("name"))


@functools.lru_cache(maxsize=8)
def get_user_by_name(name: str,
                     group: bool = False) -> typing.Optional[typing.Mapping]:
    """
    Get user info by user's name from password database.
    """
    try:
        uinfo = pwd.getpwnam(name)
        ret = dict(uid=uinfo.pw_uid, gid=uinfo.pw_gid, name=uinfo.pw_name,
                   gecos=uinfo.pw_gecos, homedir=uinfo.pw_dir, groups=[],
                   shell=uinfo.pw_shell)
        if group:
            ret["groups"] = [group["name"] for group in get_all_groups()
                             if name in group["members"]]
        return ret

    except KeyError:
        pass

    return None


@functools.lru_cache(maxsize=8)
def get_group_by_name(name: str) -> typing.Optional[typing.Mapping]:
    """
    Get group info by group's name from group database.
    """
    try:
        group = grp.getgrnam(name)
        return dict(gid=group.gr_gid, name=group.gr_name, members=group.gr_mem)

    except KeyError:
        pass

    return None


@functools.lru_cache(maxsize=8)
def get_group_by_gid(gid: int) -> typing.Optional[typing.Mapping]:
    """
    Get group info by group's gid from group database.
    """
    try:
        group = grp.getgrgid(gid)
        return dict(gid=gid, name=group.gr_name, members=group.gr_mem)

    except KeyError:
        pass

    return None

# vim:sw=4:ts=4:et:
