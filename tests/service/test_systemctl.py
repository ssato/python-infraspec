#
# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""SELinux modules tests.
"""
import random
import subprocess

import infraspec.service.systemctl as TT


def list_services_itr(status: str = "enabled"):
    cmd = "systemctl list-unit-files --type=service".split()
    ret = subprocess.check_output(cmd)

    svcs = [[col.decode("utf-8") for col in line.split()]
            for line in ret.splitlines() if b".service" in line]

    for svc in svcs:
        if svc[1] == status:
            yield svc[0]  # service unit name


def get_running_service_itr():
    svcs = list(list_services_itr())

    for svc in random.sample(svcs, len(svcs)):
        try:
            cmd = "systemctl is-active {}".format(svc).split()
            subprocess.check_call(cmd)
            yield svc
        except subprocess.CalledProcessError:
            pass


def test_is_enabled():
    svc = random.choice(list(list_services_itr()))
    assert TT.is_enabled(svc)
    assert TT.is_enabled(svc.split(".service")[0])

    svc = random.choice(list(list_services_itr("disabled")))
    assert not TT.is_enabled(svc)


def test_is_running():
    for svc in get_running_service_itr():
        assert TT.is_running(svc)
        assert TT.is_running(svc.split(".service")[0])

# vim:sw=4:ts=4:et:
