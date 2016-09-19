#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# status.py
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
#       2016-09-19T14:18:22+02:00
#           First release.
#

from threading import Lock
# from heartbeater.logging import debug

# Lock for states
lock = Lock()


class HBStatus(object):
    def __init__(self):
        # debug('HBStatus __init__()')
        with lock:
            self.master = False     # Always start as a slave
            self.electing = False   # Do not start in election mode
        # debug('HBStatus __init__() complete')

    def is_master(self):
        # debug('HBStatus is_master()')
        return self.master

    def is_electing(self):
        # debug('HBStatus is_electing()')
        return self.electing

    def is_slave(self):
        # debug('HBStatus is_slave()')
        return not ( self.master or self.electing )

    def become_master(self):
        # debug('HBStatus become_master()')
        with lock:
            self.master = True
            self.electing = False

    def start_electing(self):
        # debug('HBStatus become_electing()')
        with lock:
            self.master = False
            self.electing = True

    def become_slave(self):
        # debug('HBStatus become_slave()')
        with lock:
            self.master = False
            self.electing = False

    def to_string(self):
        # debug('HBStatus to_string()')
        with lock:
            if self.is_master():
                return 'Master'
            elif self.is_electing():
                return 'Electing'
            else:
                return 'Slave'


