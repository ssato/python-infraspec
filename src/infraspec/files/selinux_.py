#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""SELinux related.
"""
import selinux

from .common import Path


def has_selinux_label(path: Path, label: str, strict: bool = False) -> bool:
    """
    :param path: The path to target object
    :param size: Expected SELinux label
    :param strict: Exact match will be searched if True

    :return: True if the file at the path `path` has given SELinux label
    """
    # .. note::
    #    Allow partial matches like 'system_u:object_r:etc_t' vs.
    #    '...(same)...:s0' (w/ MLS attribute).
    if strict:
        return selinux.getfilecon(str(path))[-1] == label

    return selinux.getfilecon(str(path))[-1].startswith(label)

# vim:sw=4:ts=4:et:
