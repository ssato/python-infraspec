#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Common data and functions.
"""
from .custom_types import (  # noqa: F401
    Path, MountInfo, MountInfoTpl
)
from .mounts import (  # noqa: F401
    get_mounts_itr, get_mounts, get_mount_info_by_path
)

# vim:sw=4:ts=4:et:
