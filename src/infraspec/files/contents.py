#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""Loading files.
"""
import pathlib
import re
import typing

import anyconfig

from .common import Path


# .. note:: TBD
FileContentType = typing.Union[str, typing.Mapping, typing.Any, None]


def get_content(path: Path, **oargs: typing.Union[str, int]) -> str:
    """
    :param path: File path
    :raises: Error, OSError, IOError and so on
    """
    return pathlib.Path(path).read_text()


def contain(path: Path, pattern: str, **oargs: typing.Union[str, int]) -> bool:
    """
    :param path: File or dir path
    :param pattern: Regex pattern to search for

    :raises: Error, OSError, IOError and so on
    """
    reg = re.compile(pattern)

    with pathlib.Path(path).open(**oargs) as fobj:
        for line in fobj:
            if reg.search(line) is not None:
                return True

    return False


def load(path: Path, ftype: typing.Union[str, None] = None) -> FileContentType:
    """
    :param path: The path to target object
    :param filetype: Expected file type, e.g. yaml and json

    :return: Loaded content as str or an (maybe mapping) object
    """
    return anyconfig.load(path, ac_parser=ftype)

# vim:sw=4:ts=4:et:
