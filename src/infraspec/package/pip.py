#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#service
#
"""pip related functions.
"""
import functools
import json
import subprocess
import typing


def make_cmd_itr(path: typing.Optional[str] = None, outdated: bool = False,
                 ) -> typing.List[str]:
    """
    Make a list of command strings to list pip pakcages.

    >>> list(make_cmd_itr())
    ['pip', 'list', '--format=json']
    >>> list(make_cmd_itr(outdated=True))
    ['pip', 'list', '--format=json', '--outdated']
    >>> list(make_cmd_itr(False, "tmp")
    ['pip', 'list', '--format=json', '--outdated']
    """
    for cmd_s in "pip list --format=json".split():
        yield cmd_s

    if path:
        yield "--path"
        yield path

    if outdated:
        yield "--outdated"


@functools.lru_cache(maxsize=8)
def list_installed(path: typing.Optional[str] = None, outdated: bool = False
                   ) -> typing.List[typing.Mapping]:
    """
    Get the list of python packages installed using pip.
    """
    cmd = list(make_cmd_itr(path=path, outdated=outdated))
    res = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    if res.returncode == 0:
        data = res.stdout.decode("utf-8").rstrip()
        return json.loads(data)

    return []  # Just in case.


def get_installed(name: str, version: str = None) -> typing.Mapping:
    """
    Get the info of given package may be installed.
    """
    for pkg in list_installed():
        if pkg["name"] == name:
            if version is None or pkg["version"] == version:
                return pkg

    return None


def is_installed(name: str, version: str = None) -> bool:
    """
    Is the package `name` installed ?
    """
    return get_installed(name, version=version) is not None

# vim:sw=4:ts=4:et:
