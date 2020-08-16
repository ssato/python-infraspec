#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""user getter and test functions.
"""
from .linux import (  # noqa: F401
    get, exist, belong_to_group, belong_to_primary_group,
    exists, is_in_group,
    have_uid, have_home_directory, have_login_shell
)

# vim:sw=4:ts=4:et:
