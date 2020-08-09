#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
#
"""Mounts tests.
"""
import pathlib

import infraspec.common.mounts as TT


_MTAB_0 = """rootfs / rootfs rw 0 0
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
tmpfs /run tmpfs rw,seclabel,nosuid,nodev,mode=755 0 0
/dev/sda1 /boot ext4 rw,seclabel,relatime,data=ordered 0 0
"""

_MNTS_0 = [
    ("/", dict(device="rootfs", type="rootfs", options=dict(rw=True))),
    ("/proc", dict(device="proc", type="proc",
                   options=dict(rw=True, nosuid=True, nodev=True, noexec=True,
                                relatime=True))),
    ("/run", dict(device="tmpfs", type="tmpfs",
                  options=dict(rw=True, seclabel=True, nosuid=True, nodev=True,
                               mode="755"))),
    ("/boot", dict(device="/dev/sda1", type="ext4",
                   options=dict(rw=True, seclabel=True, relatime=True,
                                data="ordered")))
]


def test_get_mounts_itr__from_sys(tmpdir):
    assert list(TT.get_mounts_itr())  # Should be some results.


def test_get_mounts_itr__from_file(tmpdir):
    assert list(TT.get_mounts_itr())  # Should be some results.

    mtab = pathlib.Path(tmpdir) / "mtab"
    mtab.touch()
    assert not list(TT.get_mounts_itr(mtab))

    mtab.write_text(_MTAB_0)
    assert list(TT.get_mounts_itr(mtab)) == _MNTS_0


def test_get_mount_info_by_path(tmpdir):
    mtab = pathlib.Path(tmpdir) / "mtab"
    mtab.write_text(_MTAB_0)

    assert TT.get_mount_info_by_path("/", mtab) == _MNTS_0[0][-1]
    assert TT.get_mount_info_by_path("/boot", mtab) == _MNTS_0[-1][-1]

# vim:sw=4:ts=4:et:
