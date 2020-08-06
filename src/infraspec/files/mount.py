#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""Mounted point related.
"""
import pathlib
import typing

import psutil

from .common import Path


MountAttrs = typing.Mapping
MountInfo = typing.Union[typing.Mapping, typing.Any, None]


def _get_mount_info_using_psutil(path: pathlib.Path) -> MountInfo:
    """
    :return: psutil._common.sdiskpart object holding mount point info
    """
    mnt = [pmnt for pmnt in psutil.disk_partitions()
           if pmnt.mountpoint == str(path)]

    if not mnt:
        return None

    keys = ("device", "mountpoint", "fstype", "opts")
    return {key: getattr(mnt, key) for key in keys}


def _mnt_opts_parse_itr(opts: str) -> typing.Iterator[str]:
    """
    :return: Parse a given mount options string and make a dict hodling them
    """
    isep = ','
    kvsep = '='

    for opt in opts.split(isep):
        if kvsep in opt:
            yield tuple(opt.split(kvsep))
        else:
            yield (opt, True)


def _test_mount_attrs(path: pathlib.Path, with_: MountAttrs,
                      mnt: MountInfo = None) -> bool:
    """
    :return: True if the object at the path `path` is immutable
    """
    if mnt is None:
        mnt = _get_mount_info_using_psutil(path)  # Should be a mapping obj.

    for attr, val in with_.items():
        if attr == "opts":  # special case.
            mopts = dict(_mnt_opts_parse_itr(mnt.get("opts", "")))
            for mattr, mval in val.items():
                if mopts.get(mattr, None) != mval:
                    return False
        else:
            return mnt.get(attr, None) == val

    return True


def is_mounted(path: Path,
               with_: typing.Union[MountAttrs, None] = None) -> bool:
    """
    :return: True if the object at the path `path` is mounted
    """
    path = pathlib.Path(path)

    if with_ is None:
        return path.is_mount()

    return _test_mount_attrs(path, with_)

# vim:sw=4:ts=4:et:
