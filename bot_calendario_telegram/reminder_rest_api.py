"""rest api reminder python module.

Functions:

* get(/)
* get(/all)
* get(/number)
* get(/get/{id})
"""
# External imports
import hug
import json
from __init__ import TEST_REMINDER_DATA_PATH

with open(TEST_REMINDER_DATA_PATH, 'r') as file:
    reminder_object = json.loads(file.read())


# === Get `/` ===
@hug.get('/')
def index():
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
