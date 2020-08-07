#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""Basic file test functions.
"""
import pathlib

from .common import Path


def is_file(path: Path) -> bool:
    """
    :return: True if the object at the path `path` is a file.

    .. todo:: how much cost the overhead of pathlib.Path instead of os.path?
    """
    return pathlib.Path(path).is_file()


def exist(path: Path) -> bool:
    """
    :return: True if the object at the path `path` exist.
    """
    return pathlib.Path(path).exists()


# alias
exists = exist  # pylint: disable=invalid-name


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

# vim:sw=4:ts=4:et:
