#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""file test functions using stat(2) and so on.
"""
import enum
import hashlib
import pathlib
import typing

from .common import Path


class Checksum(enum.Enum):
    """File checksum type."""

    MD5 = hashlib.md5
    SHA1 = hashlib.sha1
    SHA256 = hashlib.sha256
    SHA512 = hashlib.sha512


def get_checksum(path: Path,
                 csum_fun: typing.Optional[Checksum] = None) -> bool:
    """
    :return: Checksum value of the file of given path
    """
    path = pathlib.Path(path)

    if csum_fun is None:
        csum_fun = Checksum.SHA256

    return csum_fun.value(path.read_bytes()).hexdigest()


def has_checksum(path: Path, csum: str,
                 csum_fun: typing.Optional[Checksum] = None) -> bool:
    """
    :return: True if the file at the path `path` has given checksum
    """
    return get_checksum(path, csum_fun=csum_fun) == csum


def get_size(path: Path) -> int:
    """
    :param path: The path to target object

    :return: True if the file at the path `path` has given size
    """
    return pathlib.Path(path).stat().st_size


def has_size(path: Path, size: int) -> bool:
    """
    :param path: The path to target object
    :param size: Expected file size in bytes

    :return: True if the file at the path `path` has given size
    """
    return get_size(path) == size

# vim:sw=4:ts=4:et:
