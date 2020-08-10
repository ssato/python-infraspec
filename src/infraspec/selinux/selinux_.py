#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://github.com/SELinuxProject/selinux
#
"""SELinux related test functions.
"""
import functools
import pathlib
import re
import typing

from ..common import Path, get_mount_info_by_path
from .constants import (
    ENFORCING, PERMISSIVE, DISABLED, POLICIES, POL_TARGETED, ROOT, CONFIG
)


_LINE_RE = re.compile(r"^(\w+)=(\w+)$")


@functools.lru_cache(maxsize=8)
def is_enabled(root: Path = ROOT) -> bool:
    """
    Determine if SELinux is enabled or not.

    .. seealso:: libselinux/src/enabled.c

    .. note:: libselinux is public domain software.
    """
    root = pathlib.Path(root)
    try:
        return root.exists() and root.is_dir() and root.is_mount()
    except AttributeError:  # pathlib.Path.is_mount is avail. >= py3.7
        pass

    return get_mount_info_by_path(root) is not None


@functools.lru_cache(maxsize=8)
def get_config(cnf_path: Path = CONFIG, root: Path = ROOT,
               cnf_line_re: typing.Pattern = _LINE_RE) -> typing.Mapping:
    """
    :return: A mapping object holding SELinux configuration info or None

    .. seealso:: libselinux/src/selinux_config.c
    """
    default = {}

    if not is_enabled(root):
        return default

    path = pathlib.Path(cnf_path)
    if not path.exists() or not path.is_file():
        return default

    return dict(cnf_line_re.match(line).groups()
                for line in pathlib.Path(cnf_path).read_text().splitlines()
                if line and not line.startswith("#"))


def get_mode(cnf_path: Path = CONFIG, root: Path = ROOT) -> str:
    """
    :return: Encorcing mode, one of enforcing, permissive and disabled
    """
    return get_config(cnf_path, root).get("SELINUX", "disabled")


def get_policy_type(cnf_path: Path = CONFIG, root: Path = ROOT) -> str:
    """
    :return: Encorcing mode, one of enforcing, permissive and disabled
    """
    return get_config(cnf_path, root).get("SELINUXTYPE", POL_TARGETED)


def is_in_mode_with_policy(cnf_path: Path = CONFIG, root: Path = ROOT,
                           mode: str = ENFORCING,
                           with_policy: typing.Optional[str] = None) -> bool:
    """
    Is it in SELinux enforcing mode?
    """
    if get_mode(cnf_path, root) != mode:
        return False

    if not with_policy:
        return True

    if with_policy not in POLICIES:
        raise ValueError("Invalid policy type: {}".format(with_policy))

    return get_policy_type(cnf_path, root) == with_policy


def is_enforcing(cnf_path: Path = CONFIG, root: Path = ROOT,
                 with_policy: typing.Optional[str] = None) -> bool:
    """
    Is it in SELinux enforcing mode with given policy optionally?
    """
    return is_in_mode_with_policy(cnf_path, root, ENFORCING, with_policy)


def is_permissive(cnf_path: Path = CONFIG, root: Path = ROOT,
                  with_policy: typing.Optional[str] = None) -> bool:
    """
    Is it in SELinux permissive mode with given policy optionally?
    """
    return is_in_mode_with_policy(cnf_path, root, PERMISSIVE, with_policy)


def is_disabled(cnf_path: Path = CONFIG, root: Path = ROOT) -> bool:
    """
    Is SELinux disabled
    """
    return not is_enabled(root) or get_mode(cnf_path, root) == DISABLED

# vim:sw=4:ts=4:et:
