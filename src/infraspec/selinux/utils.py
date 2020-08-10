#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""Utilities
"""
try:
    import selinux
    LIBSELINUX_AVAIL = True
except ImportError:
    import xattr  # https://github.com/xattr/xattr
    LIBSELINUX_AVAIL = False

from ..common import Path


def get_selinux_label(path: str) -> str:
    """
    Get file's SELinux label
    """
    if LIBSELINUX_AVAIL:
        return selinux.getfilecon(path)[-1]

    return xattr.get(path, "security.selinux").decode("utf-8")[:-1]


def has_selinux_label(path: Path, label: str, strict: bool = False) -> bool:
    """
    :param path: The path to target object
    :param size: Expected SELinux label
    :param strict: Exact match will be searched if True

    :return: True if the file at the path `path` has given SELinux label
    """
    path = str(path)

    # .. note::
    #    Allow partial matches like 'system_u:object_r:etc_t' vs.
    #    '...(same)...:s0' (w/ MLS attribute).
    if strict:
        return get_selinux_label(path) == label

    return get_selinux_label(path).startswith(label)

# vim:sw=4:ts=4:et: