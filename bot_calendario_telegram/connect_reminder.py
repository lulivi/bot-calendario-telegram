"""Provides functions to communicate with reminder through the rest api."""

# External imports
import requests

# Internal imports
import context
from bot_calendario_telegram.settings import REMINDER_REST_API_PORT

assert context


def status():
    """Return the status of the rest api."""
    return requests.get(
        'http://localhost:{0}/status'.format(REMINDER_REST_API_PORT), ).json()


def add_event(event_info):
    """Send a request to add an event."""
    return requests.post(
        'http://localhost:{0}/event/new'.format(REMINDER_REST_API_PORT),
        json=event_info,
    ).json()


def list_events():
    """List all the saved events."""
    return requests.get(
        'http://localhost:{}/event/list'.format(REMINDER_REST_API_PORT),
    ).json()
