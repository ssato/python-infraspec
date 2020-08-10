#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://github.com/SELinuxProject/selinux
#
"""SELinux common variables
"""
(ENFORCING, PERMISSIVE, DISABLED) = ("enforcing", "permissive", "disabled")
POLICIES = (POL_TARGETED, POL_MINIMUM, POL_MLS
            ) = ("targeted", "minimum", "mls")

ROOT = "/sys/fs/selinux"
CONFIG = "/etc/selinux/config"

# vim:sw=4:ts=4:et:
