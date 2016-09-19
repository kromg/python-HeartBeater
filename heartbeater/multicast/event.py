#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# multicast/event.py
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
#       2016-09-19T14:25:12+02:00
#           First release.
#

import json


# Global: charset
charset = 'utf-8'




class Event(object):

    def __init__(self, softwareID, event_status, source_address):
        self.softwareID = softwareID
        self.event_status = event_status
        self.source_address = source_address

    @staticmethod
    def from_data(data):
        return Event(
                data['ID'],
                data['EventStatus'],
                data['SrcAddress'],
                )

    def to_string(self):
        return json.dumps({
            'ID' : self.softwareID,
            'EventStatus' : self.event_status,
            'SrcAddress' : self.source_address
            })

    def to_bytes(self):
        return bytes( self.to_string(), charset )

    def is_local_to(self, softwareID, source_address):
        return (
            self.softwareID == softwareID and
            self.source_address == source_address
            )

    def is_master(self):
        return self.event_status == 'Master'




class EventGenerator(object):

    def __init__(self, softwareID, status, source_address):
        self.softwareID = softwareID
        self.status = status
        self.source_address = source_address


    def new_event(self):
        return Event(self.softwareID, self.status.to_string(), self.source_address)


    def parse_json(self, data):
        return Event.from_data( json.loads( data.decode( charset ) ) )








