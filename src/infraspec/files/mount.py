#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""Mounted point related.
"""
import pathlib
import re
import typing

from .common import Path


MountAttrs = typing.Mapping
MountInfo = typing.Union[typing.Mapping, None]


_PROC_MNT_LINE_RE = re.compile(
    r"(?P<device>\S+)\s+"
    r"(?P<mountpoint>/\S+)\s+"
    r"(?P<type>\S+)\s+"
    r"(?P<options>\S+)\s+"
)


MountTpl = typing.Tuple[str, typing.Mapping]


def _parse_proc_mounts() -> typing.Iterator[MountTpl]:
    """
    :return: A list of mapping objects each gives mount info
    """
    for line in pathlib.Path("/proc/mounts").read_text().splitlines():
        match = _PROC_MNT_LINE_RE.match(line)
        if match is None:
            continue  # Although it should not happen ...

        minfo = match.groupdict()
        opts = dict(opt.split('=') if '=' in opt else (opt, True)
                    for opt in minfo["options"].split(','))

        yield (minfo["mountpoint"],
               dict(device=minfo["device"], type=minfo["type"], options=opts))


def _get_mount_info_by_path(path: pathlib.Path) -> MountInfo:
    """
    :return: A mapping object gives mount info for given mount point
    """
    for mountpoint, minfo in _parse_proc_mounts():
        if mountpoint == str(path):
            return minfo

    return None


def _dict_included(lhs: typing.Mapping, rhs: typing.Mapping) -> bool:
    """
    :return: True if lhs is included in rhs

    >>> dic = dict(a=1, b=dict(c=2))
    >>> ref = dict(a=1, b=dict(c=2), d=dict(e="E"))
    >>> _dict_included(ref, dic)
    False
    >>> _dict_included(dic, {})
    False
    >>> _dict_included(dic, ref)
    True
    """
    for key, val in lhs.items():
        if key not in rhs or rhs[key] != val:
            return False

    return True


def _test_mount_attrs(path: pathlib.Path, with_: MountAttrs,
                      exact_match: bool = False) -> bool:
    """
    :return:
        True if the object at the path `path` is mounted with expected
        attributes
    """
    minfo = _get_mount_info_by_path(path)

    if exact_match:
        return with_ == minfo

    return _dict_included(with_, minfo)


def is_mounted(path: Path,
               with_: typing.Union[MountAttrs, None] = None,
               only_with: typing.Union[MountAttrs, None] = None) -> bool:
    """
    :return: True if the object at the path `path` is mounted
    """
    path = pathlib.Path(path)

    if with_ is None:
        return path.is_mount()

    if only_with:
        return _test_mount_attrs(path, only_with, exact_match=True)

    return _test_mount_attrs(path, with_)

# vim:sw=4:ts=4:et:
