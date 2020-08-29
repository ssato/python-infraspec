#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#service
#
"""System service related functions using systemctl.
"""
import subprocess
import typing


def rpm_query(name: str, version: str = None,
              nvrae: bool = False) -> typing.List[str]:
    r"""
    Build 'rpm -q ....' query command.

    >>> rpm_query("bash")
    ['rpm', '-q', 'bash']
    >>> rpm_query("bash", "5.0.17")
    ['rpm', '-q', 'bash-5.0.17']
    >>> rpm_query("bash", "5.0.17", nvrae=True)
    ['rpm', '-q', 'bash-5.0.17', '--qf', '"%{n},%{v},%{r},%{arch},%{e}\n"']
    """
    pkg = name if version is None else name + '-' + version

    if nvrae:
        opt = '--qf "%{n},%{v},%{r},%{arch},%{e}\n"'
        return "rpm -q {} {}".format(pkg, opt).split(sep=' ')

    return "rpm -q {}".format(pkg).split()


def get_installed(name: str, version: str = None,
                  nvrae: bool = False) -> typing.Optional[str]:
    """
    Get a package or packages list matches given name and version optionally.
    """
    cmd = rpm_query(name, version, nvrae=nvrae)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    return res.stdout.decode("utf-8").rstrip() if res.returncode == 0 else None


def is_installed(name: str, version: str = None) -> bool:
    """
    Is the package `name` installed ?
    """
    cmd = rpm_query(name, version)
    return subprocess.run(cmd, check=False).returncode == 0

# vim:sw=4:ts=4:et:
