#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""SELinux test functions.
"""
from .selinux_ import (  # noqa: F401
    is_enabled, get_config, get_mode, get_policy_type,
    is_enforcing, is_permissive, is_disabled
)
from .utils import has_selinux_label  # noqa: F401
from .modules import is_installed  # noqa: F401

# vim:sw=4:ts=4:et:
