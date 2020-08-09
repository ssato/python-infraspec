#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
"""Common data types.
"""
import pathlib
import typing


Path = typing.Union[str, pathlib.Path]

MountInfoTpl = typing.Tuple[str, typing.Mapping]
MountInfo = typing.Mapping

# vim:sw=4:ts=4:et:
