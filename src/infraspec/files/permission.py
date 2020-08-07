#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""File tests.
"""
import enum
import os
import pathlib
import re
import stat
import typing

from .common import Path


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


_MODE_RE: typing.Pattern = re.compile(r"^\d?\d{3}$")


def has_mode(path: Path, mode: str = "644",
             mode_re: typing.Pattern = _MODE_RE) -> bool:
    """
    :param path: File or dir path
    :param mode: Expected mode of the target, e.g. '755', '1644'

    :raises: FileNotFoundError, ValueError
    """
    path = pathlib.Path(path)  # Just in case, `path` is a str.

    if not mode_re.match(mode):
        raise ValueError(
            "mode must be in the form of '(0o)?[0-9]{{3}}': {}".format(mode)
        )

    mlen = len(mode)
    # '0o100644' -> '644'
    return mode[- mlen:] == oct(path.stat().st_mode)[- mlen:]


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
        access_by = ReadBy.OTHER.value

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
        access_by = WriteBy.OTHER.value

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
        access_by = ExecBy.OTHER.value

    return bool(path.stat().st_mode & access_by)


def is_immutable(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is immutable
    """
    return bool(pathlib.Path(path).stat().st_mode & stat.SF_IMMUTABLE)

# vim:sw=4:ts=4:et:
