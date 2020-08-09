#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""SELinux test functions.
"""
from .selinux_ import (  # noqa: F401
    is_selinux_enabled, get_config, get_mode, get_policy_type
)

# vim:sw=4:ts=4:et:
