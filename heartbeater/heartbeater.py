#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# heartbeater.py
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
#       2016-09-19T12:16:42+02:00
#           First release.
#

import threading
from heartbeater import hbstatus
from heartbeater.multicast import hbsender, hbwatcher
import time



# Callbacks must be implemented by the class consumer
def become_slave():
    raise NotImplementedError()


# Callbacks must be implemented by the class consumer
def become_master():
    raise NotImplementedError()


# May be implemented by the class consumer
def start_electing():
    pass



class HeartBeater(threading.Thread):

    def __init__(self, softwareID, multicast_group = '239.0.0.1', udp_port = 2016, interface_ip = '127.0.0.1',
            become_master_callback = become_master,
            become_slave_callback = become_slave,
            start_electing_callback = start_electing,   # Optional
            ):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter

        self.keep_going = True

        self.softwareID = softwareID
        self.multicast_group = multicast_group
        self.udp_port = udp_port
        self.interface_ip = interface_ip
        self.become_master_callback = become_master_callback
        self.become_slave_callback = become_slave_callback
        self.start_electing_callback = start_electing_callback


    def run(self):
        self.status = hbstatus.HBStatus()
        self.timeout = 500   # ms
        self.sender = hbsender.HBSender(
                self.softwareID,
                self.multicast_group,
                self.udp_port,
                self.interface_ip,
                self.status,
                self.timeout
                )

        self.watcher = hbwatcher.HBWatcher(
                self.softwareID,
                self.multicast_group,
                self.udp_port,
                self.interface_ip,
                self.status,
                self.timeout,
                self.become_master_callback,
                self.become_slave_callback,
                self.start_electing_callback,
                )

        self.sender.start()
        self.watcher.start()

        while (self.keep_going):
            print('LOOP')
            time.sleep(1)



    def stop(self):
        self.sender.stop()
        self.watcher.stop()
        self.keep_going = False

