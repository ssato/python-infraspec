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


(ENFORCING, PERMISSIVE, DISABLED) = ("enforcing", "permissive", "disabled")

_CNF_ROOT = "/sys/fs/selinux"
_CNF = "/etc/selinux/config"
_CNF_RE = re.compile(r"^(\w+)=(\w+)$")


@functools.lru_cache(maxsize=8)
def is_enabled(root: Path = _CNF_ROOT) -> bool:
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
def get_config(cnf_path: Path = _CNF, root: Path = _CNF_ROOT,
               cnf_line_re: typing.Pattern = _CNF_RE) -> typing.Mapping:
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


def get_mode(cnf_path: Path = _CNF, root: Path = _CNF_ROOT) -> str:
    """
    :return: Encorcing mode, one of enforcing, permissive and disabled
    """
    return get_config(cnf_path, root).get("SELINUX", "disabled")


def get_policy_type(cnf_path: Path = _CNF, root: Path = _CNF_ROOT) -> str:
    """
    :return: Encorcing mode, one of enforcing, permissive and disabled
    """
    return get_config(cnf_path, root).get("SELINUXTYPE", "targeted")

# vim:sw=4:ts=4:et:
