#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# ref. https://serverspec.org/resource_types.html#sysctl
#
"""sysctl related functions.
"""
import os
import re
import subprocess
import typing


_SYSCTL_VAL_RE = re.compile(r"^(?P<name>[a-z][^ =]+) =(?: )?(?P<value>.*)?$")


def _parse(result: str, pattern: typing.Pattern = None
           ) -> typing.Optional[typing.Tuple[str, str]]:
    """
    Parse the output of sysctl command.

    >>> _parse("")
    >>> _parse("dev.cdrom.info =")
    ('dev.cdrom.info', '')
    >>> _parse("dev.cdrom.info = drive name:")
    ('dev.cdrom.info', 'drive name:')
    >>> _parse("dev.i915.perf_stream_paranoid = 1")
    ('dev.i915.perf_stream_paranoid', '1')
    """
    if not pattern:
        pattern = _SYSCTL_VAL_RE

    match = pattern.match(result)
    return match.groups() if match else None


def _get(name: typing.Optional[str] = None
         ) -> typing.List[typing.Tuple[str, str]]:
    """
    Get all of or specific sysctl configurations.
    """
    cmd = ["sysctl"] + ([name] if name else ["-a"])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, check=False)

    if res.returncode == 0:
        data = res.stdout.decode("utf-8").split(sep=os.linesep)
        ret = [_parse(line) for line in data if line]
        return [val for val in ret if val]

    return []  # I think it should not happen but just in case.


def list() -> typing.List[typing.Tuple[str, str]]:
    """
    Get all of sysctl configurations.
    """
    return _get()


def get(name: str) -> typing.List[str]:
    """
    Get a value or values of given sysctl parameter.
    """
    results = _get(name)
    if results:
        return [param[-1] for param in results]

    return []


def is_set(name: str, value: typing.Union[str, typing.List[str]]) -> bool:
    """
    Is the given sysctl parameter set to the given value?
    """
    return get(name) == [value] if isinstance(value, str) else value

# vim:sw=4:ts=4:et:
