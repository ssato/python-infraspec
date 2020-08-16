#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import uuid

import infraspec.files.contents as TT


def test_get_content():
    assert TT.get_content(__file__)


def test_contain():
    assert TT.contain(__file__, ".+")
    assert TT.contain(__file__, "test_contain")
    assert not TT.contain(__file__, str(uuid.uuid4()))


def test_load(tmp_path):
    path = tmp_path / "test.json"
    data = dict(a=1, b=dict(c="c", d=[1, 2]))
    TT.anyconfig.dump(data, path)

    assert TT.load(path)
    assert TT.load(path) == data

# vim:sw=4:ts=4:et:
