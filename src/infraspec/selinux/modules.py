#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#file
#
"""SELinux modules
"""
import pathlib
import subprocess
import typing

from ..common import Path
from .constants import ROOT, CONFIG
from .selinux_ import get_policy_type


def get_mod_root(cnf_path: Path = CONFIG, root: Path = ROOT):
    """
    Get SELinux modules root dir to list modules.
    """
    ptype = get_policy_type(cnf_path, root)
    return pathlib.Path(
        "/var/lib/selinux/{}/active/modules/".format(ptype)
    )


def list_modules_by_path(cnf_path: Path = CONFIG,
                         root: Path = ROOT) -> typing.List[str]:
    """
    List SELinux modules.
    """
    mroot = get_mod_root(cnf_path, root)
    return [str(mod) for mod in pathlib.Path(mroot).glob("*")]


def list_modules_by_semodule() -> typing.List[str]:
    """
    List SELinux modules using semodule command.
    """
    return [
        line.rstrip() for line
        in subprocess.check_output("semodule -l".split()).splitlines()
        if line
    ]


def list_modules(use_semodule: bool = True,
                 cnf_path: Path = CONFIG,
                 root: Path = ROOT) -> typing.List[str]:
    """
    List SELinux modules.
    """
    if use_semodule:
        return list_modules_by_semodule()

    return list_modules_by_path(cnf_path, root)


def is_installed(mod: str,
                 use_semodule: bool = True,
                 cnf_path: Path = CONFIG,
                 root: Path = ROOT) -> typing.List[str]:
    """
    Test if given SELinux module is installed.
    """
    return mod in list_modules(use_semodule, cnf_path, root)

# vim:sw=4:ts=4:et:
