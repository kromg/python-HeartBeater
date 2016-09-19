#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# hbsender.py
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
#       2016-09-19T13:49:49+02:00
#           First release.
#
import threading
import socket
import struct
import sys
import time
import heartbeater.multicast.event


class HBSender(threading.Thread):

    def __init__(self, softwareID, multicast_group, udp_port, interface_ip, status, timeout):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter

        self.keep_going = True

        self.softwareID = softwareID
        self.multicast_group = multicast_group
        self.udp_port = udp_port
        self.interface_ip = interface_ip
        self.status = status
        self.timeout = timeout
        self.packet_destination = (multicast_group, udp_port)
        self.event_generator = heartbeater.multicast.event.EventGenerator(softwareID, status, interface_ip)


    def _init_socket(self):
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set the reuse address flag on the socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind on the correct interface
        sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(self.multicast_group) + socket.inet_aton(self.interface_ip)
                )

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # Set multicast loopback option to 1 so that we will receive our own
        # multicast packets - receiver will need to know if we're multicasting
        sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        return sock


    def run(self):
        sock = self._init_socket()

        while (self.keep_going):
            if (self.status.is_master() or self.status.is_electing()):
                sock.sendto( self.event_generator.new_event().to_bytes(), self.packet_destination)
            time.sleep(self.timeout / 1000)


    def stop(self):
        self.keep_going = False
