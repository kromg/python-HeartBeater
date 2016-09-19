#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# test.py
#
#     Copyright (C) 2016 Giacomo Montagner <giacomo@entirelyunlike.net>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CHANGELOG:
#
#       2016-09-19T12:22:07+02:00
#           First release.
#

import sys
sys.path.append('./')
sys.path.append('../')
import time

from heartbeater import heartbeater


def become_master():
    print('BECOMING MASTER!')

def become_slave():
    print('BECOMING SLAVE!')

def start_electing():
    print('STARTING ELECTION!')


hb = heartbeater.HeartBeater(
        softwareID = 'AppID',
        multicast_group = '239.0.0.2',
        udp_port = 2017,
        interface_ip = '127.0.0.1',
        become_master_callback = become_master,
        become_slave_callback = become_slave,
        start_electing_callback = start_electing
        )

hb.start()

while (True):
    try:
        print('TEST LOOP')
        time.sleep(2)
    except:
        print('Sayonara')
        hb.stop()
        break

print("Test OK")

