#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""File tests.
"""
import grp
import os
import pathlib
import pwd
import socket

import infraspec.files.files as TT


def test_is_file():
    assert TT.is_file(__file__)
    assert not TT.is_file(pathlib.Path(__file__).parent)


def test_exist():
    assert TT.exist(__file__)
    assert not TT.exist("./not_exist_file.txt")


def test_is_directory():
    assert TT.is_directory(pathlib.Path(__file__).parent)
    assert not TT.is_directory(__file__)


def test_is_block_device():
    bdevs = [dev for dev
             in (pathlib.Path("/dev/{}".format(dev))
                 for dev in ("vda", "vdb", "sda", "sdb", "hda", "hdb"))
             if dev.exists()]

    if not bdevs:
        raise OSError("Not block devices were found")

    assert TT.is_block_device(bdevs[0])
    assert not TT.is_block_device(__file__)


def test_is_character_deivce():
    cdevs = [cdev for cdev
             in (pathlib.Path(dev) for dev in ("/dev/ttyS0", "/dev/ttys0"))
             if cdev.exists()]

    if not cdevs:
        raise OSError("Not character devices were found")

    assert TT.is_character_deivce(cdevs[0])
    assert not TT.is_character_deivce(__file__)


def test_is_pipe(tmpdir):
    path = pathlib.Path(tmpdir) / "test.fifo"
    os.mkfifo(str(path))

    assert TT.is_pipe(path)
    assert not TT.is_pipe(__file__)


def test_is_socket(tmpdir):
    path = pathlib.Path(tmpdir) / "test.sock"

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(path))

    try:
        assert TT.is_socket(path)
        assert not TT.is_socket(__file__)
    finally:
        sock.close()


def test_is_symlink(tmpdir):
    path = pathlib.Path(tmpdir) / "test.symlink"
    os.symlink(__file__, path)

    assert TT.is_symlink(path)
    assert not TT.is_symlink(__file__)


def test_is_owned_by():
    uname = pwd.getpwuid(os.getuid()).pw_name

    assert TT.is_owned_by(__file__, uname)
    assert not TT.is_owned_by(__file__, "root")


def test_is_grouped_into():
    gname = grp.getgrgid(os.getgid()).gr_name

    assert TT.is_grouped_into(__file__, gname)
    assert not TT.is_grouped_into(__file__, "root")


def test_is_linked_to(tmpdir):
    path = pathlib.Path(tmpdir) / "test.symlink"
    path2 = (pathlib.Path(tmpdir) / "test.txt")
    os.symlink(__file__, path)

    assert TT.is_linked_to(path, __file__)

    path2.touch()
    assert not TT.is_linked_to(path2, __file__)

# vim:sw=4:ts=4:et:
