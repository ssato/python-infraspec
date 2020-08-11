#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#service
#
"""System service related functions using systemctl.
"""
import subprocess


def is_enabled(svc: str) -> bool:
    """
    Is service `svc` enabled?
    """
    ret = subprocess.run(["systemctl", "is-enabled", svc])
    return ret.returncode == 0


def is_running(svc: str) -> bool:
    """
    Is service `svc` running?
    """
    ret = subprocess.run(["systemctl", "is-active", svc])
    return ret.returncode == 0

# vim:sw=4:ts=4:et:
