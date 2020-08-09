#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Misc and utility functions to get mount info.
"""
import functools
import pathlib
import re
import typing

from .custom_types import (
    Path, MountInfo, MountInfoTpl
)


MaybeMntTblPath = typing.Optional[Path]
MaybeMntInfo = typing.Optional[MountInfo]

_PROC_MNT_LINE_RE = re.compile(
    r"(?P<device>\S+)\s+"
    r"(?P<mountpoint>\S+)\s+"
    r"(?P<type>\S+)\s+"
    r"(?P<options>\S+)\s+"
)


def get_mounts_itr(mnttbl: MaybeMntTblPath = None,
                   reg: typing.Pattern = _PROC_MNT_LINE_RE
                   ) -> typing.Iterator[MountInfoTpl]:
    """
    Parse mnt table file [/proc/mounts] and yield each mount info line by line.
    """
    # How much cost?
    mnttbl = pathlib.Path("/proc/mounts" if mnttbl is None else mnttbl)

    for line in mnttbl.read_text().splitlines():
        match = reg.match(line)
        if match is None:
            continue  # Although it should not happen ...

        minfo = match.groupdict()
        opts = dict(opt.split('=') if '=' in opt else (opt, True)
                    for opt in minfo["options"].split(','))

        yield (minfo["mountpoint"],
               dict(device=minfo["device"], type=minfo["type"], options=opts))


@functools.lru_cache(maxsize=8)
def get_mounts(mnttbl: MaybeMntTblPath = None,
               reg: typing.Pattern = _PROC_MNT_LINE_RE
               ) -> typing.List[MountInfoTpl]:
    """
    .. seealso:: above :func:`get_mounts_itr`
    """
    return [minfo for minfo in get_mounts_itr(mnttbl, reg)]


@functools.lru_cache(maxsize=8)
def get_mount_info_by_path(path: Path,
                           mnttbl: MaybeMntTblPath = None,
                           reg: typing.Pattern = _PROC_MNT_LINE_RE
                           ) -> MaybeMntInfo:
    """
    :return: A mapping object gives mount info for given mount point
    """
    if not path:
        return None

    path = pathlib.Path(path)

    if not path.exists() or not path.is_dir():
        return None

    for mountpoint, minfo in get_mounts_itr(mnttbl, reg):
        if mountpoint == str(path):
            return minfo

    return None

# vim:sw=4:ts=4:et:
