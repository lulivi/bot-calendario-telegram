# -*- coding: utf-8 -*-
"""
Provide responses for some routes in the app.

Copyright 2017, Luis Liñán (luislivilla@gmail.com)

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""

# External imports
import hug
import json
import context
from bot_calendario_telegram.settings import TESTING

assert context


with open(TESTING['REMINDER_DATA_FILE'], 'r') as file:
    reminder_object = json.loads(file.read())


# === Get `/` ===
@hug.get('/')
def index():
    """Return web status."""
    return {'status': 'OK'}


# === Get `/status` ===
@hug.get('/status')
def status():
    """Return web status."""
    return {'status': 'OK'}


# === Get `/all` ===
@hug.get('/all')
def get_all():
    """Return all evnets."""
    return reminder_object['event']


# === Get `/number` ===
@hug.get('/number')
def events_number():
    """Return the number of events."""
    return len(reminder_object['event'])


# === Get `/get/{id}` ===
@hug.get('/get/{id}')
def get_one(id: int):
    """Return one event."""
    ev = None
    for rem in reminder_object['event']:
        if rem['id_event'] == str(id):
            ev = rem
            break
    if ev is None:
        return {'id_event': None, "data_event": None}
    else:
        return ev
