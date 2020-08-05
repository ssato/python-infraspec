#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""File tests.
"""
from __future__ import absolute_import

import enum
import os
import pathlib
import re
import stat
import typing

import psutil


Path = typing.Union[str, pathlib.Path]


class ReadBy(enum.Enum):
    """File / Dir read access by who."""

    USER = stat.S_IRUSR
    GROUP = stat.S_IRGRP
    OTHER = stat.S_IROTH


class WriteBy(enum.Enum):
    """File / Dir write access by who."""

    USER = stat.S_IWUSR
    GROUP = stat.S_IWGRP
    OTHER = stat.S_IWOTH


class ExecBy(enum.Enum):
    """File / Dir exec access by who."""

    USER = stat.S_IXUSR
    GROUP = stat.S_IXGRP
    OTHER = stat.S_IXOTH


def is_file(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a file. 
    
    .. todo:: how much costs the overhead of pathlib.Path instantiation?
    """
    return pathlib.Path(path).is_file()


def exist(path: Path) -> bool:
    """
    :return: True if the object at the path `path` exist.
    """
    return pathlib.Path(path).exists()


def is_directory(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a directory.
    """
    return pathlib.Path(path).is_dir()


def is_block_device(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a block device.
    """
    return pathlib.Path(path).is_block_device()


def is_character_deivce(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a character device.
    """
    return pathlib.Path(path).is_char_device()


def is_pipe(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a named pipe (fifo) file.
    """
    return pathlib.Path(path).is_fifo()


def is_socket(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a socket file.
    """
    return pathlib.Path(path).is_socket()


def is_symlink(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a symlink file.
    """
    return pathlib.Path(path).is_symlink()


_MODE_RE: typing.Pattern = re.compile(r"^\d?\d{3}$")


def has_mode(path: Path, mode: str = "0o644",
             mode_re: typing.Pattern = _MODE_RE) -> bool:
    """
    :param path: File or dir path
    :param mode: Expected mode of the target, e.g. '755', '1644'

    :raises: FileNotFoundError, ValueError
    """
    path = pathlib.Path(path)  # Just in case, `path` is a str.

    if not mode_re.match(mode):
        raise ValueError(
            "mode must be in the form of '(0o)?[0-9]{3}': {}".format(mode)
        )

    return mode[-3:] == oct(path.stat().st_mode)[-3:]  # '0o100644' -> '644'


def contain(path: Path, pattern: str) -> bool:
    """
    :param path: File or dir path
    :param pattern: Regex pattern to search for

    :raises: Error, OSError, IOError and so on
    """
    content = pathlib.Path(path).read_text()
    return re.search(pattern, content, re.MULTILINE) is not None


def is_owned_by(path: Path, user: str) -> bool:
    """
    :return: True if the object at the path `path` is owned by the user `user`
    """
    return pathlib.Path(path).owner() == user


def is_grouped_into(path: Path, group: str) -> bool:
    """
    :return:
        True if the object at the path `path` is grouped into the group `group`
    """
    return pathlib.Path(path).group() == group


def is_linked_to(path: Path, target: Path) -> bool:
    """
    :return: True if the object at the path `path` is linked to `target`
    """
    return pathlib.Path(path).samefile(pathlib.Path(target))


def is_readable(path: Path,
                access_by: typing.Union[ReadBy, str, None] = None) -> bool:
    """
    :return: True if the object at the path `path` is readable
    """
    path = pathlib.Path(path).resolve()

    if access_by is None or (isinstance(access_by, str) and
                             access_by == path.owner()):
        return os.access(path, os.R_OK)

    if isinstance(access_by, str):
        access_by = ReadBy.OTHER

    return bool(path.stat().st_mode & access_by)


def is_writable(path: Path,
                access_by: typing.Union[WriteBy, str, None] = None) -> bool:
    """
    :return: True if the object at the path `path` is writable
    """
    path = pathlib.Path(path).resolve()

    if access_by is None or (isinstance(access_by, str) and
                             access_by == path.owner()):
        return os.access(path, os.W_OK)

    if isinstance(access_by, str):
        access_by = WriteBy.OTHER

    return bool(path.stat().st_mode & access_by)


def is_executable(path: Path,
                  access_by: typing.Union[ExecBy, str, None] = None) -> bool:
    """
    :return: True if the object at the path `path` is executable
    """
    path = pathlib.Path(path).resolve()

    if access_by is None or (isinstance(access_by, str) and
                             access_by == path.owner()):
        return os.access(path, os.X_OK)

    if isinstance(access_by, str):
        access_by = ExecBy.OTHER

    return bool(path.stat().st_mode & access_by)


def is_immutable(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is immutable
    """
    return bool(pathlib.Path(path).stat().st_mode & stat.SF_IMMUTABLE)


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


def is_mounted(path: Path, with_: typing.Union[MountAttrs, None]) -> bool:
    """
    :return: True if the object at the path `path` is immutable
    """
    path = pathlib.Path(path)

    if with_ is None:
        return path.is_mount()

    return _test_mount_attrs(path, with_)

# vim:sw=4:ts=4:et:
