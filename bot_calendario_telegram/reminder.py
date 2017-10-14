#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Remainder python module.

Checks in a data base when an event needs to be reminded.
"""

# External imports
import datetime


# === Reminder Class ===
class Reminder:
    """
    Checks and modifies a data base for geting and saving events.

    Methods:

    * save_event
    * get_event
    * next_event
    """

    def save_event(event_id, event_date):
        """Save the event in the data base."""
        pass

    def get_event(event_id):
        """Get the event from the data base."""
        pass

    def next_event(event_date=datetime.date()):
        """Check next event in the data base."""
        pass
